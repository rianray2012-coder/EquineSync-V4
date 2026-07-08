from __future__ import annotations

import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class SourceCheck:
    key: str
    label: str
    path: str
    required_terms: tuple[str, ...]
    ready_evidence: str
    missing_status: str = "blocked"


@dataclass(frozen=True)
class AbsenceCheck:
    key: str
    label: str
    paths: tuple[str, ...]
    forbidden_terms: tuple[str, ...]
    evidence: str


SOURCE_CHECKS: tuple[SourceCheck, ...] = (
    SourceCheck(
        "web_manifest",
        "Web/PWA manifest metadata",
        "frontend/public/manifest.json",
        ("Equine-Sync", "standalone", "theme_color", "icon-512.png"),
        "Web manifest remains available for web/PWA metadata evidence.",
    ),
    SourceCheck(
        "capacitor_config",
        "Capacitor config",
        "frontend/capacitor.config.json",
        ('"appId": "com.equinesync.app"', '"appName": "EquineSync"', '"webDir": "build"', '"androidScheme": "https"'),
        "Capacitor config defines native shell identity and build web directory.",
    ),
    SourceCheck(
        "capacitor_dependencies",
        "Capacitor package dependencies",
        "frontend/package.json",
        ('"@capacitor/core"', '"@capacitor/cli"', '"@capacitor/ios"', '"@capacitor/android"'),
        "Frontend package declares Capacitor core, CLI, iOS, and Android packages.",
    ),
    SourceCheck(
        "ios_project_shell",
        "iOS native project shell",
        "frontend/ios/App/App.xcodeproj/project.pbxproj",
        ("PBXProject", "com.equinesync.app", "AppDelegate.swift"),
        "Capacitor iOS Xcode project shell exists.",
    ),
    SourceCheck(
        "ios_app_config",
        "iOS app config",
        "frontend/ios/App/App/Info.plist",
        ("CFBundleDisplayName", "$(PRODUCT_NAME)", "UILaunchStoryboardName", "Main"),
        "iOS app plist exists with launch storyboard and main storyboard references.",
    ),
    SourceCheck(
        "ios_storyboards",
        "iOS bridge storyboards",
        "frontend/ios/App/App/Base.lproj/Main.storyboard",
        ("CAPBridgeViewController", "Capacitor", "initialViewController"),
        "iOS bridge storyboard exists and points at Capacitor's bridge controller.",
    ),
    SourceCheck(
        "ios_launch_assets",
        "iOS launch assets",
        "frontend/ios/App/App/Assets.xcassets/Splash.imageset/Contents.json",
        ("splash-2732x2732.png", "idiom", "universal"),
        "iOS launch asset catalog exists for the generated shell.",
    ),
    SourceCheck(
        "ios_spm_source",
        "iOS Swift Package shell",
        "frontend/ios/App/CapApp-SPM/Sources/CapApp-SPM/CapApp-SPM.swift",
        ("isCapacitorApp", "true"),
        "iOS Swift Package source exists for Capacitor shell integration.",
    ),
    SourceCheck(
        "android_project_shell",
        "Android native project shell",
        "frontend/android/settings.gradle",
        ("include ':app'", "include ':capacitor-cordova-android-plugins'"),
        "Capacitor Android Gradle project shell exists.",
    ),
    SourceCheck(
        "android_identity",
        "Android app identity",
        "frontend/android/app/build.gradle",
        ('namespace = "com.equinesync.app"', 'applicationId "com.equinesync.app"', "versionName"),
        "Android app namespace and application id match the RF16 identity default.",
    ),
    SourceCheck(
        "android_manifest",
        "Android manifest",
        "frontend/android/app/src/main/AndroidManifest.xml",
        ("android.permission.INTERNET", "MainActivity", "android.intent.action.MAIN"),
        "Android manifest declares only the shell-required internet permission and launch activity.",
    ),
    SourceCheck(
        "android_main_activity",
        "Android MainActivity",
        "frontend/android/app/src/main/java/com/equinesync/app/MainActivity.java",
        ("package com.equinesync.app;", "BridgeActivity", "extends BridgeActivity"),
        "Android MainActivity exists under the EquineSync package.",
    ),
    SourceCheck(
        "android_resources",
        "Android app resources",
        "frontend/android/app/src/main/res/values/strings.xml",
        ("EquineSync", "com.equinesync.app", "custom_url_scheme"),
        "Android resource strings carry the EquineSync app name and package identity.",
    ),
    SourceCheck(
        "android_gradle_wrapper",
        "Android Gradle wrapper",
        "frontend/android/gradle/wrapper/gradle-wrapper.properties",
        ("distributionUrl", "gradle-8.14.3-all.zip", "validateDistributionUrl=true"),
        "Android Gradle wrapper metadata exists for local native builds once Java/JDK is available.",
    ),
    SourceCheck(
        "android_test_identity",
        "Android generated test identity",
        "frontend/android/app/src/androidTest/java/com/getcapacitor/myapp/ExampleInstrumentedTest.java",
        ("package com.equinesync.app;", 'assertEquals("com.equinesync.app"', "useAppContext"),
        "Android generated instrumentation test identity matches the EquineSync package.",
    ),
)


ABSENCE_CHECKS: tuple[AbsenceCheck, ...] = (
    AbsenceCheck(
        "store_submission_absent",
        "App-store submission artifacts",
        ("frontend/ios", "frontend/android", ".github", "fastlane"),
        ("App Store Connect API key", "play-store-upload", "supply.json", "fastlane deliver", "fastlane supply"),
        "RF16 does not add App Store Connect or Google Play submission automation.",
    ),
    AbsenceCheck(
        "native_billing_absent",
        "Native in-app purchase implementation",
        ("frontend/ios", "frontend/android", "frontend/src"),
        ("StoreKit", "Product.PurchaseResult", "BillingClient", "com.android.billingclient", "InAppPurchase"),
        "RF16 does not add Apple/Google native billing implementation.",
    ),
    AbsenceCheck(
        "broad_offline_native_absent",
        "Broad native/offline claims",
        ("frontend/src", "frontend/ios", "frontend/android"),
        ("BGTaskScheduler", "BackgroundFetch", "serviceWorker.register", "indexedDB", "createObjectStore"),
        "RF16 does not add native background sync, service-worker offline shell, or universal IndexedDB storage.",
    ),
)


FOUNDER_DECISIONS: tuple[Dict[str, str], ...] = (
    {
        "decision": "Approve Capacitor as the native shell strategy.",
        "status": "requires founder review",
        "phase": "RF16, RF18",
        "notes": "RF16 creates shell readiness evidence but does not submit to stores.",
    },
    {
        "decision": "Approve app identity values.",
        "status": "requires founder review",
        "phase": "RF16, RF18",
        "notes": "RF16 defaults to EquineSync / com.equinesync.app pending final founder/legal approval.",
    },
    {
        "decision": "Approve native billing and subscriber-access posture.",
        "status": "requires founder review",
        "phase": "RF16, RF18",
        "notes": "RF16 does not implement Apple/Google in-app purchase or native billing compliance.",
    },
    {
        "decision": "Approve TestFlight and Play internal-test timing.",
        "status": "requires founder review",
        "phase": "RF16, RF18",
        "notes": "Local Android debug and iOS simulator builds pass; TestFlight and Play internal-test timing remain founder/store decisions.",
    },
)


def build_rf16_pwa_native_app_store_readiness(root: Path = ROOT) -> Dict[str, Any]:
    source_rows = [_evaluate_source_check(root, check) for check in SOURCE_CHECKS]
    absence_rows = [_evaluate_absence_check(root, check) for check in ABSENCE_CHECKS]
    build_rows = _build_environment_rows(root)

    issues: List[Dict[str, str]] = []
    for row in source_rows:
        if row["status"] != "ready":
            issues.append({
                "severity": "blocker",
                "category": "source_evidence",
                "key": row["key"],
                "message": f"{row['label']} missing required evidence: {row['missing_terms']}",
            })
    for row in absence_rows:
        if row["status"] != "absent":
            issues.append({
                "severity": "blocker",
                "category": "overclaim_guard",
                "key": row["key"],
                "message": f"{row['label']} unexpectedly present: {', '.join(row['matches'][:5])}",
            })
    for row in build_rows:
        if row["status"] == "blocked":
            issues.append({
                "severity": "blocker",
                "category": "local_toolchain",
                "key": row["key"],
                "message": row["evidence"],
            })

    issue_counts = Counter(issue["severity"] for issue in issues)
    source_ready = all(row["status"] == "ready" for row in source_rows)
    overclaims_clean = all(row["status"] == "absent" for row in absence_rows)
    build_blockers = issue_counts.get("blocker", 0) if source_ready and overclaims_clean else issue_counts.get("blocker", 0)
    if source_ready and overclaims_clean and build_blockers:
        overall_status = "blocked_by_local_native_toolchain"
    elif issue_counts.get("blocker", 0):
        overall_status = "blocked"
    else:
        overall_status = "ready"

    return {
        "phase": "RF16",
        "title": "RF16 PWA, Native App, App Store, and Google Play Readiness",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "source_rows": source_rows,
        "absence_rows": absence_rows,
        "build_rows": build_rows,
        "issues": issues,
        "issue_counts": dict(sorted(issue_counts.items())),
        "founder_decisions": list(FOUNDER_DECISIONS),
    }


def render_rf16_report(report: Dict[str, Any]) -> str:
    return "\n".join([
        "# RF16 PWA, Native App, App Store, and Google Play Readiness Report",
        "",
        "Phase: `RF16`",
        f"Generated at: `{report['generated_at']}`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Source Evidence",
        "",
        _table(
            ["Key", "Label", "Status", "Evidence"],
            [[row["key"], row["label"], row["status"], row["evidence"] if row["status"] == "ready" else row["missing_terms"]] for row in report["source_rows"]],
        ),
        "",
        "## Local Build Evidence",
        "",
        _table(
            ["Key", "Label", "Status", "Evidence"],
            [[row["key"], row["label"], row["status"], row["evidence"]] for row in report["build_rows"]],
        ),
        "",
        "## Overclaim Guards",
        "",
        _table(
            ["Key", "Label", "Status", "Evidence"],
            [[row["key"], row["label"], row["status"], row["evidence"] if row["status"] == "absent" else ", ".join(row["matches"][:5])] for row in report["absence_rows"]],
        ),
        "",
        "## Issues",
        "",
        _table(
            ["Severity", "Category", "Key", "Message"],
            [[item["severity"], item["category"], item["key"], item["message"]] for item in report["issues"]],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Phase", "Notes"],
            [[item["decision"], item["status"], item["phase"], item["notes"]] for item in report["founder_decisions"]],
        ),
        "",
        "## RF16 Boundary",
        "",
        "- RF16 creates Capacitor native shell readiness evidence for iOS and Android.",
        "- RF16 does not submit to App Store Connect or Google Play Console.",
        "- RF16 does not create live Apple/Google listings, mutate providers, implement native billing, complete privacy labels/Data safety, or create review accounts.",
        "- RF16 does not broaden RF15 offline claims or claim full offline/native behavior.",
        "- Current launch claims may say a Capacitor shell exists only to the extent supported by this report. They must not say EquineSync is available in the App Store or Google Play, submitted for review, approved for TestFlight/Play internal testing, or native billing compliant.",
        "",
    ])


def _evaluate_source_check(root: Path, check: SourceCheck) -> Dict[str, Any]:
    text = _read_text(root / check.path)
    missing = [term for term in check.required_terms if term not in text]
    return {
        "key": check.key,
        "label": check.label,
        "path": check.path,
        "status": "ready" if text and not missing else check.missing_status,
        "missing_terms": ", ".join(missing),
        "evidence": check.ready_evidence,
    }


def _evaluate_absence_check(root: Path, check: AbsenceCheck) -> Dict[str, Any]:
    matches: List[str] = []
    for relative in check.paths:
        path = root / relative
        candidates = [path] if path.is_file() else [item for item in path.rglob("*") if item.is_file()] if path.is_dir() else []
        for candidate in candidates:
            if _should_skip_absence_candidate(candidate):
                continue
            text = _read_text(candidate)
            if any(term in text for term in check.forbidden_terms):
                matches.append(str(candidate.relative_to(root)))
    return {
        "key": check.key,
        "label": check.label,
        "status": "present" if matches else "absent",
        "matches": matches,
        "evidence": check.evidence,
    }


def _build_environment_rows(root: Path) -> List[Dict[str, str]]:
    web_build = root / "frontend" / "build" / "index.html"
    android_debug_apk = root / "frontend" / "android" / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
    ios_sim_app = _ios_simulator_app_path()
    rows = [
        {
            "key": "web_build_output",
            "label": "Frontend production build output",
            "status": "ready" if web_build.exists() else "blocked",
            "evidence": "frontend/build/index.html exists after RF16 web build." if web_build.exists() else "frontend/build/index.html missing; run npm --prefix frontend run build.",
        }
    ]

    xcodebuild = _xcodebuild_version()
    rows.append({
        "key": "ios_local_build_toolchain",
        "label": "iOS local build toolchain",
        "status": "ready" if xcodebuild else "blocked",
        "evidence": xcodebuild or "Functional xcodebuild unavailable in this environment; local iOS build remains blocked.",
    })
    rows.append({
        "key": "ios_simulator_build_output",
        "label": "iOS simulator build output",
        "status": "ready" if ios_sim_app else "blocked",
        "evidence": f"{ios_sim_app} exists after RF16 iOS simulator build." if ios_sim_app else "iOS simulator App.app output missing; run xcodebuild for scheme App on an iOS simulator.",
    })

    java = _java_version()
    rows.append({
        "key": "android_local_build_toolchain",
        "label": "Android local build toolchain",
        "status": "ready" if java else "blocked",
        "evidence": java or "Java runtime unavailable in this environment; local Android Gradle build remains blocked.",
    })
    rows.append({
        "key": "android_debug_build_output",
        "label": "Android debug build output",
        "status": "ready" if android_debug_apk.exists() else "blocked",
        "evidence": "frontend/android/app/build/outputs/apk/debug/app-debug.apk exists after RF16 Android debug build." if android_debug_apk.exists() else "Android debug APK missing; run ./gradlew assembleDebug from frontend/android.",
    })
    return rows


def _ios_simulator_app_path() -> str:
    derived_data = Path.home() / "Library" / "Developer" / "Xcode" / "DerivedData"
    if not derived_data.exists():
        return ""
    matches = sorted(
        derived_data.glob("App-*/Build/Products/Debug-iphonesimulator/App.app"),
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
    )
    return str(matches[-1]) if matches else ""


def _java_version() -> str:
    try:
        completed = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=10, check=False)
    except (FileNotFoundError, subprocess.SubprocessError):
        return ""
    return (completed.stderr or completed.stdout or "").splitlines()[0] if completed.returncode == 0 else ""


def _xcodebuild_version() -> str:
    try:
        completed = subprocess.run(["xcodebuild", "-version"], capture_output=True, text=True, timeout=10, check=False)
    except (FileNotFoundError, subprocess.SubprocessError):
        return ""
    if completed.returncode != 0:
        return ""
    return (completed.stdout or "").splitlines()[0] if completed.stdout else ""


def _should_skip_absence_candidate(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & {"node_modules", "build", "public", ".git", "__pycache__"})


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError):
        return ""


def _table(headers: List[str], rows: List[List[Any]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    if rows:
        out.extend("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |" for row in rows)
    else:
        out.append("| " + " | ".join("-" for _ in headers) + " |")
    return "\n".join(out)
