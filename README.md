# Huxley Apartment Watch

Monitors [Huxley Apartments](https://www.equityapartments.com/san-francisco-bay/redwood-city/huxley-apartments) in Redwood City for two-bedroom availability and sends an email notification when units become available.

## How It Works

- GitHub Actions runs twice daily (9am and 9pm PST)
- Checks the Huxley website for two-bedroom availability
- Tracks state between runs to avoid duplicate notifications
- Sends a single email when availability changes from unavailable to available

## Setup

1. Fork this repository
2. Add the following secrets in **Settings → Secrets and variables → Actions**:
   - `EMAIL_FROM` - Gmail address to send from
   - `EMAIL_PASSWORD` - [Gmail app password](https://myaccount.google.com/apppasswords)
   - `EMAIL_TO` - Email address to receive notifications

3. Enable Actions in your fork if not already enabled

## Manual Trigger

You can manually run the check anytime:
1. Go to **Actions** → **Check Huxley Availability**
2. Click **Run workflow**

## Local Testing

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python huxley_monitor.py
```

Exit codes:
- `0` - Two-bedroom available
- `1` - Not available
- `2` - Error
