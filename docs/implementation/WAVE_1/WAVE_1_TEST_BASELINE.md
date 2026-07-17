# Wave 1 Test Baseline

The W1-RF01 run passed 52 unit tests. The 42 unavailable tests were HTTP integration cases in `test_phase2c_auth.py` and `test_admin_portal_admin3.py`, configured for a local API at port 8001 and isolated Mongo through `MONGO_URL`/`DB_NAME`.

Authorized startup procedure:

1. Start `mongod` with an isolated `/tmp` dbpath on localhost.
2. Start `uvicorn server:app` from `backend` with synthetic database name, strong test JWT secret, non-production environment, and port 8001.
3. Run focused and full suites against synthetic records.
4. Stop both processes and remove temporary data.

No production endpoint or credential is required.

