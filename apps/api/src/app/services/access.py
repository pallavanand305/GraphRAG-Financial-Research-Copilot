from uuid import UUID
from typing import List

class AccessService:
    def allowed_team_ids(self, user) -> List[UUID]:
        ids = []
        if hasattr(user, 'team_memberships'):
            for m in user.team_memberships:
                ids.append(m.team_id)
        return ids

    def can_view_document(self, user, doc) -> bool:
        if getattr(user, 'is_admin', False):
            return True
        allowed = set(self.allowed_team_ids(user))
        if doc.owner_team_id in allowed:
            return True
        if doc.visibility == 'org':
            return True
        if doc.visibility == 'groups':
            # simplified
            return False
        return False

access_service = AccessService()
