#!/usr/bin/env python3
"""CGP-001 placeholder validator for Validate Guide Questions."""

from __future__ import annotations

import argparse
import sys

STATUS = "NOT_IMPLEMENTED_CGP_002_REQUIRED"


def main(argv=None):
    parser = argparse.ArgumentParser(description="CGP-001 placeholder validator.")
    parser.add_argument("--substantive", action="store_true", help="Request substantive validation.")
    parser.add_argument("--status", action="store_true", help="Print placeholder status.")
    parser.parse_args(argv)
    print(f"{__file__}: {STATUS}. CGP-002 is required before substantive validation is available.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
