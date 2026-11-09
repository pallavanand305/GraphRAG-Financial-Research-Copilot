import enum

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RoleEnum(str, enum.Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"


class DocStatus(str, enum.Enum):
    uploaded = "uploaded"
    parsing = "parsing"
    indexed = "indexed"
    failed = "failed"


class DocVisibility(str, enum.Enum):
    team = "team"
    org = "org"
    groups = "groups"
