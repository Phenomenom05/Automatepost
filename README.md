# Claude Playwright Automation

Automate interaction with [Claude AI Artifacts](https://claude.ai/public/artifacts/3e407d20-4645-42a0-b1ba-b3636087f841) using [Playwright](https://playwright.dev/) to programmatically fill and submit posts, handle potential Cloudflare challenges, and verify successful submission.

---

## 🚀 Features

- Navigates to Claude AI artifact page and waits for dynamic iframe content.
- 
- Interacts robustly with iframe elements to:
  - Click "Create Post" tab/button.
  - Fill form fields (`Title`, `Content`, `Author`).
  - Submit new posts.
- Scrolls intelligently to interact with elements not initially visible.
- Verifies successful post creation by checking post counts and new post content.
- Runs Chromium in headed mode with anti-detection flags.

---

## 🛠️ Prerequisites

- Python 3.8+
- [Playwright](https://playwright.dev/python/) with Chromium browser installed.

---

## ⚡ Setup

1. Clone this repository:

bash
git clone https://github.com/yourusername/claude-playwright-automation.git
cd claude-playwright-automation

2. Install Dependencies: 
pip install playwright

3. Install Chromium Browser for Playwright:
   playwright install chromium
USAGE:
After installing all the dependencies, run :
  python claude_playwright_persistent.py


