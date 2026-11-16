#!/usr/bin/env python3
"""
Capture screenshots of key EcoCircle pages for README documentation.
Run this while the Flask server is running on localhost:5000.
"""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

# Configuration
BASE_URL = "http://localhost:5000"
SCREENSHOTS_DIR = Path(__file__).parent
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Pages to capture: (url_path, filename, description)
PAGES = [
    ("/", "01_landing_page.png", "Landing page with 3D globe"),
    ("/login.html", "02_login_page.png", "Login/Register page with Face Unlock"),
    ("/dashboard.html", "03_dashboard.png", "User Dashboard with stats & leaderboard"),
    ("/ai-engine.html", "04_ai_engine.png", "AI Vision Analysis page"),
    ("/products.html", "05_my_items.png", "My Items (Products) page"),
]

async def capture_page(page, url, filename, description):
    """Capture a screenshot of a page."""
    full_url = BASE_URL + url
    print(f"[CAPTURE] {description} ({full_url})")

    try:
        await page.goto(full_url, wait_until="networkidle", timeout=30000)
        # Wait a bit for any animations/3D globe to render
        await page.wait_for_timeout(2000)

        # Take screenshot
        filepath = SCREENSHOTS_DIR / filename
        await page.screenshot(path=str(filepath), full_page=True)
        print(f"   [OK] Saved: {filepath}")
        return True
    except Exception as e:
        print(f"   [FAIL] {e}")
        return False

async def main():
    print("Starting screenshot capture for EcoCircle...")
    print(f"Screenshots will be saved to: {SCREENSHOTS_DIR}")
    print(f"Target server: {BASE_URL}")
    print()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        success_count = 0
        for url, filename, description in PAGES:
            if await capture_page(page, url, filename, description):
                success_count += 1

        await browser.close()

        print()
        print(f"Done! Captured {success_count}/{len(PAGES)} screenshots.")
        print(f"Check: {SCREENSHOTS_DIR}")

if __name__ == "__main__":
    asyncio.run(main())