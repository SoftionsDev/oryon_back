import logging
from decimal import Decimal
from typing import Callable, Any

from django.apps import apps
from pyparsing import Word, alphanums, nums, oneOf, infixNotation, opAssoc, OneOrMore, Combine, \
    Optional, ParseResults, Literal, Group, ParseException, pyparsing_common, alphas, quotedString, removeQuotes

from brm.exceptions import InvalidExpression
from brm.models import Rule
from sales.models import Sale

logger = logging.getLogger(__name__)


COMPARISON_FUNCTIONS = {
    '=': (lambda x, y: x == y),
    '>=': (lambda x, y: x >= y),
    '<=': (lambda x, y: x <= y),
    '>': (lambda x, y: x > y),
    '<': (lambda x, y: x < y),
    '!=': (lambda x, y: x != y),
    'and': (lambda x, y: x and y),
    'or': (lambda x, y: x or y)
}


MATH_FUNCTIONS = {
    '+': (lambda x, y: x + y),
    '-': (lambda x, y: x - y),
    '*': (lambda x, y: x * y),
    '/': (lambda x, y: x / y)
}


model_fields_cache = {}

def find_model_by_name(model_name):
    model_name = model_name.lower()
    for model in apps.get_models():
        model_class_name = model.__name__.lower()
        if not model_class_name == model_name:
            continue
        return model


def get_model_fields(model_name):
    if model_name in model_fields_cache:
        return model_fields_cache[model_name]

    model = find_model_by_name(model_name)
    if not model:
        return []
    model_fields_cache[model] = [f.name for f in model._meta.get_fields()]
    return model_fields_cache[model]


def data_lookup(query: str, sale: Sale) -> Any:
    """
        Performs a dynamic lookup on the Sale object or its related objects based on a query.

        Args:
        query (str): A string in the format 'field.accessor' to specify the attribute to retrieve.
        sale (Sale): The Sale object on which the lookup is performed.

        Returns:
        Any: The value of the specified attribute.

        Raises:
        AttributeError: If the query does not correspond to a valid attribute.
        """

    related_fields_mapping = {
        'city': 'store.city',
        'region': 'store.city.region'
    }

    field, accessor = query.split('.')
    if hasattr(sale, accessor):
        return getattr(sale, accessor)

    _field = getattr(sale, field, None)
    if _field is not None:
        return getattr(_field, accessor, None)

    related_field = related_fields_mapping.get(field)
    if related_field:
        parts = related_field.split('.')
        for part in parts:
            if not hasattr(sale, part):
                return False
            sale = getattr(sale, part)

        return getattr(sale, accessor)

    # if query lookup does not exists
    return False


def rule_parser():
    word = Word(alphanums + '_').set_whitespace_chars(' ')
    field = Combine(word + OneOrMore(Literal('.') + word))

    string_value = quotedString.set_parse_action(removeQuotes)

    numeric_value = Combine(
        Optional(oneOf('+ -')) + Word(nums) + Optional(Literal('.') + Word(nums))
    )
    value = word | numeric_value | string_value
    operator = oneOf('= >= <= < > !=')
    logical_operator = oneOf('and or')

    comparison = Group(field + operator + value)

    # Define the expression
    expression = infixNotation(
        comparison,
        [
            (logical_operator, 2, opAssoc.LEFT),
        ]
    )

    return expression


def formula_parser():
    word = Word(alphanums)
    field = Combine(word + OneOrMore(Literal('.') + word))
    number = Combine(
        pyparsing_common.integer + Optional('.' + pyparsing_common.integer),
    )
    variable = Word(alphas, alphanums + "_")

    operators = oneOf('+ - * /')

    operand = field | number | variable

    # Define the expression parser
    expr = infixNotation(
        operand,
        [
            (operators, 2, opAssoc.LEFT),
        ]
    )
    return Optional(operators) + expr


def is_compound_expression(expression):
    return any(isinstance(item, ParseResults) for item in expression) and \
        any(isinstance(item, str) for item in expression)



class ExpressionValidator:

    active_rules: list = []
    default_exception = 'rule has not a proper structure'

    def __init__(self):
        self.validator_parser = rule_parser()
        self.__pre_load_active_rules()

    def __pre_load_active_rules(self):
        for rule in Rule.objects.all():
            [_rule] = self.validator_parser.parse_string(rule.expression)
            self.active_rules.append(_rule)

    def validate(self, parsed_rule: list[ParseResults]):
        for expression in parsed_rule:
            if not isinstance(expression, ParseResults):
                continue

            # validates if there is a rule with the same expression
            if any(
                expression.as_list() in rule.as_list()
                for rule in self.active_rules
            ):
                msg = f'expression {expression.as_list()} is already contained in another rule'
                logger.exception(msg)
                raise InvalidExpression(msg)

            model, field = expression[0].split('.')
            model_fields = get_model_fields(model)
            if not model_fields:
                logger.exception(self.default_exception)
                raise InvalidExpression(self.default_exception)
            if field in model_fields:
                continue
            raise InvalidExpression(self.default_exception)

    def validate_expression(self, rule):
        try:
            [parsed_rule] = self.validator_parser.parse_string(rule)
            self.validate(parsed_rule)
            return parsed_rule
        except ParseException as e:
            logger.exception(str(e))
            logger.error('Incorrect rule expression')
            raise


class RuleHandler:

    def __init__(self, data_lookup: Callable):
        self.data_lookup = data_lookup
        self.parser = rule_parser()

    def parse(self, rule: Rule):
        if not isinstance(rule, Rule):
            raise TypeError('rule must be an instance of Rule')
        try:
            [expression] = self.parser.parse_string(rule.expression)
            return expression
        except ParseException as e:
            logger.error('rule execution error')
            logger.exception(str(e))
            raise

    def run(self, expression, sale):
        if not expression:
            return False

        if not is_compound_expression(expression):
            return self._evaluate_comparison(expression, sale)

        result = self._evaluate_comparison(expression[0], sale)

        for i in range(1, len(expression), 2):
            operator = expression[i]
            next_comparison = expression[i + 1]

            # return the respective function based on the keyword operand
            operator_function = COMPARISON_FUNCTIONS.get(operator)
            result = operator_function(
                result, self._evaluate_comparison(next_comparison, sale)
            )

        return result

    def _evaluate_comparison(self, expression, sale: Sale):
        left, operand, right = expression
        left = data_lookup(left, sale)
        if isinstance(left, str):
            left = left.lower()
        if isinstance(left, Decimal):
            right = Decimal(right)

        operand = COMPARISON_FUNCTIONS.get(operand)
        return operand(left, right)


class FormulaValidator:

    default_exception = 'formula has not a proper structure'

    def __init__(self):
        self.parser = formula_parser()

    def validate_expression(self, formula):
        try:
            parsed_formula = self.parser.parse_string(formula, parseAll=True)
            self._validate(parsed_formula)
            return parsed_formula
        except ParseException as e:
            logger.exception(str(e))
            logger.error('Incorrect formula expression')
            raise

    def _validate(self, parsed_formula):
        for element in range(1, len(parsed_formula)):
            model, field = parsed_formula[element][0].split('.')  # first element contain the field accessor
            model_fields = get_model_fields(model)
            if not model_fields:
                logger.exception(self.default_exception)
                raise InvalidExpression(self.default_exception)
            if field not in model_fields:
                logger.exception(self.default_exception)
                raise InvalidExpression(self.default_exception)


class FormulaHandler:

    def __init__(self, data_lookup: Callable):
        self.parser = formula_parser()
        self.data_lookup = data_lookup

    def parse(self, rule: Rule):
        try:
            parsed_formula = self.parser.parse_string(rule.formula, parseAll=True)
            return self.load_percentages(parsed_formula, rule)
        except ParseException as e:
            logger.exception(str(e))
            logger.error('formula execution error')
            raise

    def load_percentages(self, parsed_formula, rule):
        for element in range(1, len(parsed_formula)):
            formula = parsed_formula[element].as_list()
            index = formula.index('rule.percentage')
            try:
                formula[index] = rule.percentage
            except ValueError:
                continue
            parsed_formula[element] = ParseResults(formula)
        return parsed_formula

    def run(self, parsed_formula, sale):
        if len(parsed_formula) == 2:
            operand = MATH_FUNCTIONS.get(parsed_formula[0])
            return operand(sale.price, self.run(parsed_formula[1], sale))

        left, operand, right = parsed_formula
        if isinstance(left, str):
            left = data_lookup(left, sale)
        if right.isalpha():
            right = data_lookup(right, sale)
        else:
            right = Decimal(right)

        return MATH_FUNCTIONS.get(operand)(left, right)


class RulesExecutor:

    def __init__(self, data_lookup: Callable):
        self.rule_handler = RuleHandler(data_lookup)
        self.formula_handler = FormulaHandler(data_lookup)

    def execute(self, rule: Rule, sale: Sale):
        try:
            parsed_rule = self.rule_handler.parse(rule)
            parsed_formula = self.formula_handler.parse(rule)
        except ParseException as e:
            logger.exception(str(e))
            logger.error('Incorrect rule expression')
            raise

        if not self.rule_handler.run(parsed_rule, sale):
            return False

        return self.formula_handler.run(parsed_formula, sale)

