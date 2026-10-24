from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime
from app.models.base import Base, RoleEnum, DocStatus, DocVisibility

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    entra_object_id = Column(String, unique=True)
    email = Column(String, nullable=False)
    display_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Team(Base):
    __tablename__ = "teams"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    name = Column(String, nullable=False)
    entra_group_id = Column(String, unique=True, nullable=True)
    description = Column(String)

class UserGroup(Base):
    __tablename__ = "user_groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    name = Column(String, nullable=False)
    entra_group_id = Column(String, unique=True, nullable=True)

class TeamMembership(Base):
    __tablename__ = "team_memberships"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), primary_key=True)
    role = Column(Enum(RoleEnum), nullable=False)

class UserGroupMembership(Base):
    __tablename__ = "user_group_memberships"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("user_groups.id"), primary_key=True)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    owner_team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    sha256 = Column(String, nullable=False)
    status = Column(Enum(DocStatus), default=DocStatus.uploaded)
    visibility = Column(Enum(DocVisibility), default=DocVisibility.team)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('owner_team_id', 'sha256', name='uq_doc_team_sha'),)

class DocumentGroupAccess(Base):
    __tablename__ = "document_group_access"
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), primary_key=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("user_groups.id"), primary_key=True)

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    page = Column(Integer)
    section = Column(String)
    text_hash = Column(String)

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"))
    role = Column(String)
    content = Column(Text)
    citations = Column(JSONB)
    latency_ms = Column(Integer)
    tokens_in = Column(Integer)
    tokens_out = Column(Integer)
    cost_usd = Column(JSONB)

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String)
    resource_type = Column(String)
    resource_id = Column(String)
    ip = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    details = Column(JSONB)

class FinancialFact(Base):
    __tablename__ = "financial_facts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company = Column(String)
    fiscal_year = Column(Integer)
    metric = Column(String)
    value = Column(JSONB)
    unit = Column(String)
    source_document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))

class EvalRun(Base):
    __tablename__ = "eval_runs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    git_sha = Column(String)
    dataset = Column(String)
    faithfulness = Column(JSONB)
    answer_relevance = Column(JSONB)
    context_precision = Column(JSONB)
    p95_latency_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
