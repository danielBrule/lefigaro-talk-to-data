#!/usr/bin/env python3
"""
Script to automatically test all FastAPI endpoints.
This script starts the server and tests all endpoints to ensure they work.
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def start_server():
    """Start the FastAPI server in the background."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    return subprocess.Popen(
        [
            ".venv/Scripts/python.exe",
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--log-level",
            "error",
        ],
        env=env,
        cwd=str(project_root),
    )


def test_endpoints():
    """Test all API endpoints."""
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        "/api/v0/articles",
        "/api/v0/keywords",
        "/api/v0/contributors",
        "/api/v0/errors",
        "/api/v0/version",
    ]

    print("Testing FastAPI endpoints...")
    results = []

    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            status = (
                "✓ PASS"
                if response.status_code == 200
                else f"✗ FAIL ({response.status_code})"
            )
            print(f"{status}: {endpoint}")
            results.append(
                (
                    endpoint,
                    response.status_code,
                    response.text[:100] if response.status_code != 200 else "OK",
                )
            )
        except requests.exceptions.RequestException as e:
            print(f"✗ FAIL: {endpoint} - {e}")
            results.append((endpoint, "ERROR", str(e)))

    return results


def main():
    print("Starting FastAPI server for testing...")

    # Start the server
    server_process = start_server()

    # Wait for server to start
    time.sleep(3)

    try:
        # Test the endpoints
        results = test_endpoints()

        # Summary
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)

        passed = sum(1 for _, status, _ in results if status == 200)
        total = len(results)

        for endpoint, status, details in results:
            print(f"{endpoint}: {'PASS' if status == 200 else f'FAIL ({status})'}")

        print(f"\nPassed: {passed}/{total}")

        if passed == total:
            print("🎉 All endpoints are working!")
            return 0
        else:
            print("❌ Some endpoints failed.")
            return 1

    finally:
        # Stop the server
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    sys.exit(main())
