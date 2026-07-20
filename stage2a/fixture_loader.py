#!/usr/bin/env python3
"""Synthetic-only fixture loader/reset/digest CLI for Stage 2A."""
from __future__ import annotations

import argparse, json
from lib.control import RUNTIME, cleanup, load_env, load_fixture, mongo_client, state_digest

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("action",choices=["load","digest","reset"]); p.add_argument("--fail-after",type=int); p.add_argument("--pause-after",type=int); a=p.parse_args()
    env=load_env(); client=mongo_client(env); db=client[env["DB_NAME"]]
    try:
        if a.action=="load": result=load_fixture(db,fail_after=a.fail_after,pause_after=a.pause_after,interruption_marker=RUNTIME/"fixture-interruption.marker")
        elif a.action=="digest": result={"state_digest":state_digest(db)}
        else: result=cleanup(db)
        print(json.dumps(result,indent=2,sort_keys=True))
    finally: client.close()
