from enum import Enum


class SalesTypes(Enum):
    SELF = 'propia'
    REFERRED = 'referido'
    DELIVER = 'entrega'
    OTHER = 'otros'


class CommissionTypes(Enum):
    SALE = 'venta'
    DELIVERY = 'entrega'
    OTHER = 'otros'
