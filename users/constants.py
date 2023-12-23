from enum import Enum


class Groups(str, Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    COLLABORATOR = 'collaborator'


class GoalTypes(str, Enum):

    DAILY = 'daily'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'


class Positions(Enum):
    DIRECTOR = 'director'
    ADVISER = 'asesor'
    ASSISTANT = 'asistente'
