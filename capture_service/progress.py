"""Record confirmed collection receipts for a portal scope."""
def initialize(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS portal_progress (
      collection TEXT NOT NULL, scope TEXT NOT NULL, body_sha256 TEXT NOT NULL,
      source_url TEXT NOT NULL, recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY(collection,scope,body_sha256))""")
    connection.commit()

def record(connection, collection, scope, digest, url):
    initialize(connection)
    with connection:
        connection.execute(
            'INSERT OR IGNORE INTO portal_progress(collection,scope,body_sha256,source_url) VALUES(?,?,?,?)',
            (collection,scope,digest,url))

def receipts(connection, collection):
    initialize(connection)
    return [dict(scope=row[0], body_sha256=row[1], source_url=row[2])
            for row in connection.execute(
                'SELECT scope,body_sha256,source_url FROM portal_progress WHERE collection=? ORDER BY scope',
                (collection,))]
