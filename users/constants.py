from enum import Enum


class Groups(str, Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    COLLABORATOR = 'collaborator'