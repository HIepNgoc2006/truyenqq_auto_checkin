# TruyenQQ Auto Check-in Bot 🤖

An automated daily check-in bot for TruyenQQ built with **Python**, **Playwright**, and **GitHub Actions**. This bot runs 24/7 completely free in the cloud, automatically updates to the latest active domain, and requires no local setup.

## ✨ Key Features
- **100% Automated Background Execution**: Uses GitHub Actions to run the bot daily (default is 00:30 UTC / 07:30 AM ICT).
- **Auto Domain Discovery**: The bot automatically scrapes and finds the latest active TruyenQQ domain (e.g., `truyenqqko.com`, etc.).
- **Anti-Expiration Auto Login**: Uses your Email and Password to securely log in by simulating a real user browser session, completely solving the issue of expired or reset cookies.
- **Cross-Platform Notifications**: Automatically sends check-in results via Telegram or Discord.

---

## 🚀 Setup Guide for Beginners

You don't need any coding knowledge or local installations. Just follow these 2 steps:

### Step 1: Fork this Repository
1. Log in to your GitHub account.
2. Look at the top right corner of this page and click the **Fork** button.
3. Click **Create fork** to copy this entire repository to your personal account.

### Step 2: Configure Login Credentials (Secrets)
To let the bot know which account to check in for, you need to provide your login credentials. GitHub will heavily encrypt and hide this information; **even you won't be able to view the password after entering it**.

1. Go to the Repository you just forked.
2. Click on the **Settings** tab in the horizontal menu.
3. In the left sidebar menu, scroll down to the **Security** section, select **Secrets and variables** -> **Actions**.
4. Click the green **New repository secret** button to add the following 2 mandatory variables:
   - **Name:** `TRUYENQQ_EMAIL` | **Secret:** *Your TruyenQQ account email*
   - **Name:** `TRUYENQQ_PASSWORD` | **Secret:** *Your TruyenQQ account password*

*(Make sure to enter the variable names exactly as shown above, in ALL CAPS).*

### Step 3: (Optional) Receive Check-in Notifications
If you want the bot to send you a daily report message, create the following Secrets:

**For Discord:**
- **Name:** `DISCORD_WEBHOOK_URL` | **Secret:** *Your Discord channel Webhook URL*

**For Telegram:**
- **Name:** `TELEGRAM_BOT_TOKEN` | **Secret:** *Your bot token from @BotFather*
- **Name:** `TELEGRAM_CHAT_ID` | **Secret:** *Your Telegram ID (Get it from @userinfobot)*

---

## 🛠️ How to Test the Bot Immediately
By default, the bot runs automatically every day. To check if the bot works right now:
1. Go to the **Actions** tab on your Repository.
2. (First time only) Click the green button **"I understand my workflows, go ahead and enable them"**.
3. On the left sidebar, click **TruyenQQ Daily Check-in**.
4. Click the dropdown button **Run workflow** (on the right) -> Click the green **Run workflow** button.
5. Wait a few seconds and refresh the page, then click on the running workflow to view the check-in logs.

## ⚠️ Security Notice
- This source code is completely open-source. You can freely inspect the code in the `main.py` file. Your password is never sent to anyone other than the official TruyenQQ login servers.
- If you are still concerned, you can register a secondary TruyenQQ account using a throwaway email to test it out.

---
