import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# --- API Configuration ---
# Mandatory: Your Google API Key for Gemini.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# --- Email Recipient Configuration ---
# Mandatory: Email address of the recipient.
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

# --- Email Sender Configuration ---
# Mandatory: Email address of the sender.
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
# Mandatory: Password for the sender's email account.
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

# --- SMTP Server Configuration ---
# Mandatory: SMTP server address.
SMTP_SERVER = os.environ.get("SMTP_SERVER")
# Mandatory: SMTP server port.
SMTP_PORT_STR = os.environ.get("SMTP_PORT")

SMTP_PORT = None
if SMTP_PORT_STR:
    try:
        SMTP_PORT = int(SMTP_PORT_STR)
    except ValueError:
        # This message is important for the user to debug configuration issues.
        print(f"Warning: SMTP_PORT ('{SMTP_PORT_STR}') is not a valid integer. Please check your .env file or environment variables.")
        # SMTP_PORT remains None, which should be handled by the main script.
else:
    # This handles the case where SMTP_PORT is not set at all.
    print("Warning: SMTP_PORT is not set. Please check your .env file or environment variables.")

# For informational purposes, a quick check and summary (optional, can be removed in production)
if __name__ == '__main__':
    print("Configuration loaded:")
    print(f"  GOOGLE_API_KEY: {'Set' if GOOGLE_API_KEY else 'Not Set'}")
    print(f"  RECIPIENT_EMAIL: {RECIPIENT_EMAIL}")
    print(f"  SENDER_EMAIL: {SENDER_EMAIL}")
    print(f"  SENDER_PASSWORD: {'Set' if SENDER_PASSWORD else 'Not Set'}") # Avoid printing password
    print(f"  SMTP_SERVER: {SMTP_SERVER}")
    print(f"  SMTP_PORT: {SMTP_PORT}")
    if SMTP_PORT is None and SMTP_PORT_STR: # If string was set but conversion failed
        print(f"  (Original SMTP_PORT_STR: '{SMTP_PORT_STR}' caused a conversion error)")
    elif SMTP_PORT is None:
        print(f"  (SMTP_PORT was not set in environment)")
