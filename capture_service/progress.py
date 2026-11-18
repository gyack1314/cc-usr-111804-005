from .ledger import entities
from .domain import assess
"""记录门户范围内已确认的采集收据。"""
def initialize(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS portal_sources (
      collection TEXT NOT NULL, scope TEXT NOT NULL, card_kind TEXT NOT NULL,
      required INTEGER NOT NULL, PRIMARY KEY(collection,scope,card_kind))""")
    connection.execute("""CREATE TABLE IF NOT EXISTS portal_progress (
      collection TEXT NOT NULL, scope TEXT NOT NULL, body_sha256 TEXT NOT NULL,
      source_url TEXT NOT NULL, recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY(collection,scope,body_sha256))""")
    connection.commit()

def register(connection, collection, expected):
    """登记待采的页面范围与卡片来源类别。"""
    initialize(connection)
    with connection:
        for item in expected:
            connection.execute(
                'INSERT INTO portal_sources(collection,scope,card_kind,required) VALUES(?,?,?,?) '
                'ON CONFLICT(collection,scope,card_kind) DO UPDATE SET required=excluded.required',
                (collection,item['scope'],item['kind'],int(item.get('required',True))))

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

def coverage(connection, collection):
    """Distinguish a stored portal receipt from a verified business source."""
    initialize(connection)
    rows=connection.execute(
        'SELECT s.scope,s.card_kind,s.required,COUNT(p.body_sha256) '
        'FROM portal_sources s LEFT JOIN portal_progress p '
        'ON p.collection=s.collection AND p.scope=s.scope '
        'WHERE s.collection=? GROUP BY s.scope,s.card_kind,s.required ORDER BY s.scope,s.card_kind',
        (collection,)).fetchall()
    view=assess(entities(connection,collection))
    verified={source for pair in view['matched_pairs']
              for source in (pair['left_source'],pair['right_source'])}
    sources=[]
    for scope,kind,required,received in rows:
        source_hashes={r[0] for r in connection.execute(
            'SELECT body_sha256 FROM portal_progress WHERE collection=? AND scope=?',
            (collection,scope))}
        sources.append(dict(scope=scope,kind=kind,required=bool(required),
                            received_versions=received,verified=bool(source_hashes & verified)))
    return {'expected':len(rows),'received':sum(bool(row[3]) for row in rows),
            'missing_required':[dict(scope=row[0],kind=row[1]) for row in rows if row[2] and not row[3]],
            'unverified_required':[dict(scope=item['scope'],kind=item['kind']) for item in sources
                                   if item['required'] and not item['verified']],
            'sources':sources}
