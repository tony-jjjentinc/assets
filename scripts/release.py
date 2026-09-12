#!/usr/bin/env python3
"""
JJJEI Core Assets - Automated Release Script
Handles semantic version bumping, CSS compilation, git commit, tag creation,
remote synchronization (main + latest branch), and CDN cache purging.

Usage:
    python3 scripts/release.py [patch | minor | major | <x.y.z>] [--dry-run]
"""

import argparse
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)


def run_cmd(cmd, check=True, dry_run=False):
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
    print(f"  [EXEC] {cmd_str}")
    if dry_run:
        return ""
    res = subprocess.run(cmd, shell=isinstance(cmd, str), text=True, capture_output=True)
    if check and res.returncode != 0:
        print(f"  ❌ Error executing: {cmd_str}")
        print(f"  STDERR: {res.stderr}")
        print(f"  STDOUT: {res.stdout}")
        sys.exit(res.returncode)
    return res.stdout.strip()


def parse_semver(version_str):
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_str.strip())
    if not match:
        raise ValueError(f"Invalid semver: '{version_str}'. Must follow X.Y.Z format.")
    return [int(x) for x in match.groups()]


def compute_next_version(current_version, bump_type):
    major, minor, patch = parse_semver(current_version)
    bump = bump_type.lower()
    if bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    elif bump == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump == "major":
        return f"{major + 1}.0.0"
    else:
        parse_semver(bump_type)
        return bump_type


def main():
    parser = argparse.ArgumentParser(description="Release a new version of JJJEI Core Assets.")
    parser.add_argument(
        "bump",
        nargs="?",
        default="patch",
        help="Bump type ('patch', 'minor', 'major') or explicit version (e.g. '4.1.0'). Default: 'patch'",
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulate release steps without committing or pushing.")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow running with uncommitted changes.")

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  JJJEI Core Assets — Automated Release Pipeline")
    print("=" * 60)

    # 1. Verify branch and git status
    current_branch = run_cmd("git rev-parse --abbrev-ref HEAD")
    if current_branch != "main" and not args.dry_run:
        print(f"❌ Releases must be cut from the 'main' branch (current: '{current_branch}').")
        sys.exit(1)

    status_output = run_cmd("git status --porcelain")
    if status_output and not args.allow_dirty and not args.dry_run:
        print("❌ Working directory has uncommitted changes:")
        print(status_output)
        print("Commit or stash your changes before releasing, or pass --allow-dirty.")
        sys.exit(1)

    # 2. Read package.json
    package_json_path = os.path.join(PROJECT_ROOT, "package.json")
    with open(package_json_path, "r") as f:
        pkg_data = json.load(f)

    current_ver = pkg_data.get("version", "4.0.0")
    next_ver = compute_next_version(current_ver, args.bump)

    print(f"  Current Version : v{current_ver}")
    print(f"  Target Version  : v{next_ver}")
    print(f"  Dry Run         : {'Yes' if args.dry_run else 'No'}\n")

    if current_ver == next_ver:
        print(f"⚠️ Target version is identical to current version (v{current_ver}). Aborting.")
        sys.exit(1)

    # 3. Update package.json
    pkg_data["version"] = next_ver
    if not args.dry_run:
        with open(package_json_path, "w") as f:
            json.dump(pkg_data, f, indent=2)
            f.write("\n")
        print(f"✅ Updated package.json version to {next_ver}")
    else:
        print(f"[Dry-Run] Would update package.json to {next_ver}")

    # 4. Compile all CSS bundles (colors/latest and colors/vX)
    print("\n[Step 1/5] Compiling SCSS bundles via scripts/generator.py...")
    run_cmd([sys.executable, "scripts/generator.py"], dry_run=args.dry_run)

    # 5. Git Stage and Commit
    print("\n[Step 2/5] Creating release commit...")
    run_cmd(["git", "add", "package.json", "colors/"], dry_run=args.dry_run)
    run_cmd(["git", "commit", "-m", f"RELEASE: v{next_ver}"], dry_run=args.dry_run)

    # 6. Git Tagging
    tag_name = f"v{next_ver}"
    print(f"\n[Step 3/5] Creating release tag '{tag_name}'...")
    run_cmd(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], dry_run=args.dry_run)

    # 7. Push to GitHub (main, tag, and latest branch sync)
    print("\n[Step 4/5] Pushing to GitHub (main, tag, latest branch)...")
    run_cmd(["git", "push", "origin", "main"], dry_run=args.dry_run)
    run_cmd(["git", "push", "origin", tag_name], dry_run=args.dry_run)
    run_cmd(["git", "push", "origin", "main:latest", "--force"], dry_run=args.dry_run)
    print(f"✅ Synced 'main' branch to 'latest' branch and pushed tag '{tag_name}'")

    # 8. Purge CDN
    print("\n[Step 5/5] Purging jsDelivr edge caches...")
    run_cmd([sys.executable, "scripts/purge_cdn.py"], dry_run=args.dry_run)

    print("\n" + "=" * 60)
    print(f"  🎉 Release {tag_name} Successfully Published!")
    print(f"  • Pinned Tag CDN : https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@{tag_name}/colors/latest/<group>.css")
    print(f"  • Rolling Latest : https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@latest/colors/latest/<group>.css")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
