from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.models.all import Organization, User, Team, UserGroup, TeamMembership, UserGroupMembership, Role, UserRole
from app.models.base import RoleEnum
import os
import uuid

def seed():
    engine = create_engine(os.getenv("DATABASE_URL", "postgresql+psycopg://grc:grc@localhost:5432/grc"))
    with Session(engine) as s:
        org = Organization(name="Demo Org")
        s.add(org)
        s.flush()
        t1 = Team(org_id=org.id, name="Research", entra_group_id="g-research")
        t2 = Team(org_id=org.id, name="Risk", entra_group_id="g-risk")
        s.add_all([t1,t2]); s.flush()
        g1 = UserGroup(org_id=org.id, name="all-analysts", entra_group_id="g-all-analysts")
        g2 = UserGroup(org_id=org.id, name="auditors", entra_group_id="g-auditors")
        s.add_all([g1,g2]); s.flush()
        for r in ['admin','engineer','analyst','viewer']:
            s.add(Role(name=r))
        s.flush()
        for i,email in enumerate(['admin@demo.com','eng@demo.com','res@demo.com','risk@demo.com','view@demo.com']):
            u = User(org_id=org.id, email=email, display_name=email.split('@')[0], entra_object_id=f"oid{i}")
            s.add(u); s.flush()
        s.commit()
    print("seeded")

if __name__ == "__main__":
    seed()
