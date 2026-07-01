from enum import Enum


class BoardRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"