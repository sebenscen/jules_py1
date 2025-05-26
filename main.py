import google.generativeai as genai
from src.phrase_generator import get_inspirational_phrase
from src.email_sender import send_email
from config import settings # Import the settings module

def main():
    """
    Main function to get an inspirational phrase and email it.
    Uses configuration from config.settings.
    """
    # 1. Use configuration from config.settings
    # These are already loaded from .env (if present) and environment variables by settings.py

    # 2. Validate required configuration variables from settings
    # Note: settings.py already prints warnings if SMTP_PORT conversion fails or is not set.
    # Here, we primarily check if mandatory variables are None.
    
    error_messages = []
    if not settings.GOOGLE_API_KEY:
        error_messages.append("GOOGLE_API_KEY is not set.")
    if not settings.RECIPIENT_EMAIL:
        error_messages.append("RECIPIENT_EMAIL is not set.")
    if not settings.SENDER_EMAIL:
        error_messages.append("SENDER_EMAIL is not set.")
    if not settings.SENDER_PASSWORD:
        error_messages.append("SENDER_PASSWORD is not set.")
    if not settings.SMTP_SERVER:
        error_messages.append("SMTP_SERVER is not set.")
    if settings.SMTP_PORT is None: # This covers both not set and conversion error in settings.py
        error_messages.append(f"SMTP_PORT is not valid or not set (original value: '{settings.SMTP_PORT_STR}').")

    if error_messages:
        print("Error: Missing or invalid configuration:")
        for msg in error_messages:
            print(f"  - {msg}")
        print("Please check your .env file or environment variables.")
        return

    # SMTP_PORT is now an integer or None, as handled by settings.py.
    # The check above ensures it's not None before proceeding.

    # 3. Set up Gemini API key
    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        print("Gemini API key configured.")
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        return

    # 4. Get inspirational phrase
    print("Fetching inspirational phrase...")
    phrase_details = get_inspirational_phrase()

    if phrase_details:
        print(f"Successfully fetched phrase: \"{phrase_details['phrase']}\" by {phrase_details['author']}")
        
        # 5. Send email
        print(f"Sending email to {settings.RECIPIENT_EMAIL}...")
        email_sent = send_email(
            phrase_details=phrase_details,
            recipient_email=settings.RECIPIENT_EMAIL,
            sender_email=settings.SENDER_EMAIL,
            sender_password=settings.SENDER_PASSWORD,
            smtp_server=settings.SMTP_SERVER,
            smtp_port=settings.SMTP_PORT # This is now guaranteed to be an int if we passed the checks
        )

        if email_sent:
            print("Email sent successfully!")
        else:
            print("Failed to send email.")
    else:
        print("Failed to retrieve inspirational phrase.")

if __name__ == '__main__':
    main()
