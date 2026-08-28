from __future__ import annotations

from scripts import seed_local_demo_test_accounts as seed


class FakeCollection:
    def __init__(self):
        self.docs = []

    def find_one(self, filt, projection=None):
        for doc in self.docs:
            if all(doc.get(key) == value for key, value in filt.items()):
                if projection:
                    return {key: value for key, value in doc.items() if projection.get(key)}
                return dict(doc)
        return None

    def update_one(self, filt, update, upsert=False):
        existing = self.find_one(filt)
        if existing is None:
            doc = dict(filt)
            doc.update(update.get("$setOnInsert", {}))
        else:
            doc = existing
            self.docs.remove(existing)
        doc.update(update.get("$set", {}))
        self.docs.append(doc)


class FakeDb:
    def __init__(self):
        self._collections = {}

    def __getattr__(self, name):
        return self._collection(name)

    def __getitem__(self, name):
        return self._collection(name)

    def _collection(self, name):
        self._collections.setdefault(name, FakeCollection())
        return self._collections[name]


class FakeMongoClient:
    def __init__(self, db):
        self.db = db

    def __getitem__(self, name):
        return self.db


def test_fd12_local_demo_seed_writes_selectable_account_context_memberships(monkeypatch):
    db = FakeDb()
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DB_NAME", "equinesync_fd12_seed_test")
    monkeypatch.setenv("MONGO_URL", "mongodb://127.0.0.1:27017")
    monkeypatch.setattr(seed, "MongoClient", lambda _url: FakeMongoClient(db))
    monkeypatch.setattr(seed, "_hash_pwd", lambda _password: "hashed-demo-password")
    monkeypatch.setattr(seed.sys, "argv", ["seed_local_demo_test_accounts.py", "--allow-non-test-db"])

    assert seed.main() == 0

    memberships = db.account_memberships.docs
    assert len(memberships) == len(seed.DEMO_USERS)
    assert all(row["source"] == "users_mirror" for row in memberships)
    assert all(row["membership_status"] == "active" for row in memberships)
    assert all(row["role_status"] == "active" for row in memberships)
    assert all("status" not in row for row in memberships)

    facility_rows = [row for row in memberships if row["account_type"] == "facility"]
    assert facility_rows
    assert all(row["account_id"] == "primary" for row in facility_rows)
    assert all(row["barn_id"] == "primary" for row in facility_rows)
    assert all(row["is_primary"] is True for row in facility_rows)

    standalone = [
        row for row in memberships
        if row["user_id"] == db.users.find_one({"email": "individual-owner@equinesync.com"})["id"]
    ][0]
    assert standalone["account_type"] == "individual_owner"
    assert standalone["account_id"].startswith("acct_owner_")
    assert standalone["barn_id"] is None
    assert standalone["relationship_type"] == "owner"
