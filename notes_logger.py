import argparse, sqlite3, os, uuid, csv, hashlib, datetime, json

DBFILE = os.path.join(os.getcwd(), "notes.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    created_utc TEXT,
    tz TEXT,
    author TEXT,
    category TEXT,
    amount REAL,
    currency TEXT,
    description TEXT,
    attachment_path TEXT,
    metadata TEXT,
    entry_hash TEXT
);
CREATE INDEX IF NOT EXISTS idx_notes_created ON notes(created_utc);
"""

def init_db():
    conn = sqlite3.connect(DBFILE, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()

def compute_hash(d):
    s = json.dumps(d, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def add_entry(author, category, amount, currency, description, attachment, tz):
    init_db()
    conn = sqlite3.connect(DBFILE)
    cur = conn.cursor()
    nid = str(uuid.uuid4())
    created = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    data = {
        "id": nid,
        "created_utc": created,
        "tz": tz or "UTC",
        "author": author,
        "category": category,
        "amount": amount,
        "currency": currency,
        "description": description,
        "attachment_path": attachment
    }
    entry_hash = compute_hash(data)
    cur.execute("""
        INSERT INTO notes (id, created_utc, tz, author, category, amount, currency, description, attachment_path, metadata, entry_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nid, created, data["tz"], author, category, amount, currency, description, attachment, json.dumps({}), entry_hash))
    conn.commit()
    conn.close()
    print(f"ADDED {nid} {created} HASH:{entry_hash}")

def export_csv(outpath):
    init_db()
    conn = sqlite3.connect(DBFILE)
    cur = conn.cursor()
    cur.execute("SELECT id, created_utc, tz, author, category, amount, currency, description, attachment_path, entry_hash FROM notes ORDER BY created_utc")
    rows = cur.fetchall()
    conn.close()
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","created_utc","tz","author","category","amount","currency","description","attachment_path","entry_hash"])
        w.writerows(rows)
    print(f"exported {len(rows)} rows -> {outpath}")

def show(limit):
    init_db()
    conn = sqlite3.connect(DBFILE)
    cur = conn.cursor()
    cur.execute("SELECT id, created_utc, author, category, amount, currency, description FROM notes ORDER BY created_utc DESC LIMIT ?", (limit,))
    for r in cur.fetchall():
        print(r)
    conn.close()

def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd")
    a_add = sp.add_parser("add")
    a_add.add_argument("--author", required=True)
    a_add.add_argument("--category", required=True)
    a_add.add_argument("--amount", type=float, default=None)
    a_add.add_argument("--currency", default="USD")
    a_add.add_argument("--desc", dest="description", default="")
    a_add.add_argument("--attach", dest="attachment", default=None)
    a_add.add_argument("--tz", default=None)
    sp.add_parser("show").add_argument("--limit", type=int, default=20)
    sp.add_parser("export").add_argument("--out", required=True)
    args = p.parse_args()
    if args.cmd == "add":
        add_entry(args.author, args.category, args.amount, args.currency, args.description, args.attachment, args.tz)
    elif args.cmd == "show":
        show(args.limit)
    elif args.cmd == "export":
        export_csv(args.out)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
