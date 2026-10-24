from sqlalchemy import event
from sqlalchemy.engine import Engine

def set_app_context(conn, user_id=None, team_ids=None, is_admin=False):
    if team_ids:
        conn.execute("SET LOCAL app.team_ids = '%s'" % ','.join(str(t) for t in team_ids))
    else:
        conn.execute("SET LOCAL app.team_ids = ''")
    conn.execute("SET LOCAL app.is_admin = '%s'" % ('true' if is_admin else 'false'))

@event.listens_for(Engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    pass
