from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, JSON, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime
import enum

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
