from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from core.rf16_pwa_native_app_store_readiness import (
    ROOT,
    build_rf16_pwa_native_app_store_readiness,
    render_rf16_report,
)


def test_rf16_source_shell_evidence_is_present():
    report = build_rf16_pwa_native_app_store_readiness(ROOT)

    assert {row["status"] for row in report["source_rows"]} == {"ready"}
    source_keys = {row["key"] for row in report["source_rows"]}
    assert {
        "web_manifest",
        "capacitor_config",
        "capacitor_dependencies",
        "ios_project_shell",
        "ios_app_config",
        "ios_storyboards",
        "ios_launch_assets",
        "ios_spm_source",
        "android_project_shell",
        "android_identity",
        "android_manifest",
        "android_main_activity",
        "android_resources",
        "android_gradle_wrapper",
        "android_test_identity",
    }.issubset(source_keys)


def test_rf16_records_local_native_toolchain_blockers_without_source_blockers():
    report = build_rf16_pwa_native_app_store_readiness(ROOT)

    assert report["overall_status"] in {"ready", "blocked_by_local_native_toolchain"}
    assert not [
        issue for issue in report["issues"]
        if issue["category"] in {"source_evidence", "overclaim_guard"}
    ]
    build_statuses = {row["key"]: row["status"] for row in report["build_rows"]}
    assert build_statuses["web_build_output"] == "ready"
    assert "ios_local_build_toolchain" in build_statuses
    assert "ios_simulator_build_output" in build_statuses
    assert "android_local_build_toolchain" in build_statuses
    assert "android_debug_build_output" in build_statuses


def test_rf16_overclaim_guards_are_absent():
    report = build_rf16_pwa_native_app_store_readiness(ROOT)

    assert {row["status"] for row in report["absence_rows"]} == {"absent"}


def test_rf16_capacitor_identity_values_match_native_shells():
    config = (ROOT / "frontend/capacitor.config.json").read_text(encoding="utf-8")
    android = (ROOT / "frontend/android/app/build.gradle").read_text(encoding="utf-8")
    pbxproj = (ROOT / "frontend/ios/App/App.xcodeproj/project.pbxproj").read_text(encoding="utf-8")
    android_test = (ROOT / "frontend/android/app/src/androidTest/java/com/getcapacitor/myapp/ExampleInstrumentedTest.java").read_text(encoding="utf-8")

    assert '"appId": "com.equinesync.app"' in config
    assert '"appName": "EquineSync"' in config
    assert 'namespace = "com.equinesync.app"' in android
    assert 'applicationId "com.equinesync.app"' in android
    assert "com.equinesync.app" in pbxproj
    assert "package com.equinesync.app;" in android_test
    assert 'assertEquals("com.equinesync.app"' in android_test


def test_rf16_rendered_report_has_boundaries_and_no_secret_shapes():
    rendered = render_rf16_report(build_rf16_pwa_native_app_store_readiness(ROOT))

    assert "## Source Evidence" in rendered
    assert "## Local Build Evidence" in rendered
    assert "does not submit to App Store Connect or Google Play Console" in rendered
    assert "does not broaden RF15 offline claims" in rendered
    assert not re.search(r"sk_(live|test)_[A-Za-z0-9]{16,}", rendered)
    assert not re.search(r"rk_(live|test)_[A-Za-z0-9]{16,}", rendered)
    assert not re.search(r"mongodb(\\+srv)?://[^\\s<]+:[^\\s<]+@", rendered)


def test_rf16_script_writes_report(tmp_path):
    output = tmp_path / "rf16_report.md"
    package = tmp_path / "rf16_package.zip"
    result = subprocess.run(
        [
            sys.executable,
            "backend/scripts/build_rf16_pwa_native_app_store_readiness.py",
            "--output",
            str(output),
            "--zip-output",
            str(package),
            "--fail-on-source-blockers",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()
    assert package.exists()
    assert "RF16 PWA, Native App, App Store, and Google Play Readiness Report" in output.read_text(encoding="utf-8")
    assert "source_blockers=0" in result.stdout
    assert "RF16 package written:" in result.stdout

    with ZipFile(package) as zf:
        names = set(zf.namelist())
    assert "frontend/android/app/src/main/java/com/equinesync/app/MainActivity.java" in names
    assert "frontend/android/gradle/wrapper/gradle-wrapper.properties" in names
    assert "frontend/android/gradle/wrapper/gradle-wrapper.jar" in names
    assert "frontend/android/app/src/main/res/values/strings.xml" in names
    assert "frontend/ios/App/App/Base.lproj/Main.storyboard" in names
    assert "frontend/ios/App/App/Base.lproj/LaunchScreen.storyboard" in names
    assert "frontend/ios/App/CapApp-SPM/Sources/CapApp-SPM/CapApp-SPM.swift" in names
    assert not any("/public/" in name for name in names)
    assert not any("/node_modules/" in name for name in names)


def test_rf16_proof_code_does_not_mutate_external_state():
    files = [
        ROOT / "backend/core/rf16_pwa_native_app_store_readiness.py",
        ROOT / "backend/scripts/build_rf16_pwa_native_app_store_readiness.py",
    ]
    joined = "\n".join(path.read_text(encoding="utf-8") for path in files)

    forbidden_tokens = [
        "MongoClient",
        "AsyncIOMotorClient",
        "insert_one",
        "update_one",
        "delete_one",
        "replace_one",
        "requests.",
        "httpx.",
        "stripe.",
        "founder_accepted",
    ]
    for token in forbidden_tokens:
        assert token not in joined
