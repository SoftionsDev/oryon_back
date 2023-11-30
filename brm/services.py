import logging
from decimal import Decimal
from typing import Callable, Any

from django.apps import apps
from pyparsing import Word, alphanums, nums, oneOf, infixNotation, opAssoc, OneOrMore, Combine, \
    Optional, Suppress, ParseResults, Literal, Group, ParseException

from brm.exceptions import InvalidExpression
from sales.models import Sale

logger = logging.getLogger(__name__)


OPERATOR_FUNCTIONS = {
    '=': (lambda x, y: x == y),
    '>=': (lambda x, y: x >= y),
    '<=': (lambda x, y: x <= y),
    '>': (lambda x, y: x > y),
    '<': (lambda x, y: x < y),
    '!=': (lambda x, y: x != y),
    'and': (lambda x, y: x and y),
    'or': (lambda x, y: x or y)
}


def find_model_by_name(model_name):
    model_name = model_name.lower()
    for model in apps.get_models():
        model_class_name = model.__name__.lower()
        if not model_class_name == model_name:
            continue
        return model


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
    field, accessor = query.split('.')
    if hasattr(sale, accessor):
        return getattr(sale, accessor)

    field = getattr(sale, field, None)
    if field is not None:
        return getattr(field, accessor, None)

    # if query lookup does not exists
    return False


def create_expression_parser():
    word = Word(alphanums)
    field = Combine(word + OneOrMore(Literal('.') + word))
    numeric_value = Combine(
        Optional(oneOf('+ -')) + Word(nums) + Optional(Literal('.') + Word(nums))
    )
    value = word | numeric_value
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

def create_validation_parser():

    word = Word(alphanums + '_')
    valid_word = Combine(word + OneOrMore(Literal('.') + word))
    number = Combine(Optional(oneOf('+ -')) + Word(nums))
    operator = oneOf('= > < >= <= !=')

    logical_operator = OneOrMore(oneOf('and or'))

    ignored = word | number | operator | logical_operator
    ignored_parser = Suppress(ignored)

    parser = OneOrMore(valid_word | ignored_parser)
    return parser



class ExpressionValidator:

    def __init__(self):
        self.parser = create_expression_parser()
        self.validator_parser = create_validation_parser()

    @staticmethod
    def validate_fields(expression: ParseResults):
        for field in expression:
            try:
                model, field = field.split('.')
            except ValueError as e:
                logger.error(str(e))
                raise
            model = find_model_by_name(model)
            if not model:
                raise InvalidExpression('rule has not a proper structure')
            if field in [f.name for f in model._meta.get_fields()]:
                continue
            raise InvalidExpression('rule has not a proper structure')

    def validate_expression(self, expression):
        try:
            validated_expression = self.validator_parser.parse_string(expression)
            self.validate_fields(validated_expression)
            return validated_expression
        except ParseException as e:
            logger.exception(str(e))
            logger.error('Incorrect rule expression')
            raise


class RuleExecutor:

    def __init__(self, data_lookup: Callable):
        self.data_lookup = data_lookup
        self.parser = create_expression_parser()

    def execute_rule(self, expr_string, sale: Sale):
        try:
            [expression] = self.parser.parseString(expr_string, parseAll=True)
            return self.execute_expression(expression, sale)

        except ParseException as e:
            logger.error('rule execution error')
            logger.exception(str(e))
            raise

    def execute_expression(self, expression, sale):
        if not expression:
            return False

        result = self._evaluate_comparison(expression[0], sale)

        for i in range(1, len(expression), 2):
            operator = expression[i]
            next_comparison = expression[i + 1]

            # return the respective function based on the keyword operand
            operator_function = OPERATOR_FUNCTIONS.get(operator)
            result = operator_function(
                result, self._evaluate_comparison(next_comparison, sale)
            )

        return result

    def _evaluate_comparison(self, expression, sale: Sale):
        left, operand, right = expression
        left = data_lookup(left, sale)
        if isinstance(left, Decimal):
            right = Decimal(right)

        operand = OPERATOR_FUNCTIONS.get(operand)
        return operand(left, right)

