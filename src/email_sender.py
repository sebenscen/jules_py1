import smtplib
from email.mime.text import MIMEText
import datetime

def send_email(phrase_details, recipient_email, sender_email, sender_password, smtp_server, smtp_port):
    """
    Sends an email with an inspirational phrase.

    Args:
        phrase_details (dict): A dictionary containing 'phrase', 'author', and 'location'.
        recipient_email (str): The email address of the recipient.
        sender_email (str): The email address of the sender.
        sender_password (str): The password for the sender's email account.
        smtp_server (str): The SMTP server address.
        smtp_port (int): The SMTP server port.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        # 1. Get current date
        current_date = datetime.date.today().strftime("%Y-%m-%d")

        # 2. Format email body
        phrase = phrase_details.get('phrase', 'No phrase provided.')
        author = phrase_details.get('author', 'Unknown author.')
        location = phrase_details.get('location') # Can be None

        body = f"Today's inspirational phrase ({current_date}):\n\n"
        body += f'"{phrase}"\n'
        body += f"- {author}\n"
        if location:
            body += f"(Location: {location})\n"

        # 3. Construct MIMEText object
        msg = MIMEText(body, 'plain')
        msg['Subject'] = "Your Daily Inspirational Phrase"
        msg['From'] = sender_email
        msg['To'] = recipient_email

        # 4. Connect to SMTP server and send email
        # Using SMTP_SSL for implicit SSL connection (typically port 465)
        # If port 587 is typically used, smtplib.SMTP() and server.starttls() would be more appropriate.
        # The choice depends on the specific SMTP server configuration.
        # For this implementation, we'll assume SMTP_SSL is suitable if a standard SSL port is provided.
        
        # Decision: Use SMTP_SSL if port is 465, otherwise use SMTP and try STARTTLS.
        # This makes the function more flexible.
        
        if smtp_port == 465: # Standard port for SMTPS (SSL)
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else: # Standard port for SMTP with STARTTLS is 587
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo() # Say hello to server
            server.starttls() # Secure the connection
            server.ehlo() # Re-say hello over secure connection

        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        print(f"Email sent successfully to {recipient_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"Error: SMTP Authentication failed for {sender_email}. Check credentials.")
        return False
    except smtplib.SMTPConnectError:
        print(f"Error: Could not connect to SMTP server {smtp_server}:{smtp_port}.")
        return False
    except smtplib.SMTPServerDisconnected:
        print(f"Error: SMTP server disconnected unexpectedly.")
        return False
    except smtplib.SMTPException as e:
        # Catch other SMTPlib specific errors
        print(f"SMTP Error: {e}")
        return False
    except Exception as e:
        # Catch any other non-SMTP exceptions
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == '__main__':
    # This is an example, DO NOT RUN without proper configuration
    # and be careful with credentials.
    # Set environment variables or use a config file for sensitive data in a real app.
    #
    # TEST_SENDER_EMAIL = "your_email@example.com"
    # TEST_SENDER_PASSWORD = "your_password"
    # TEST_RECIPIENT_EMAIL = "recipient_email@example.com"
    #
    # # Example for Gmail (requires App Password if 2FA is enabled)
    # # SMTP_SERVER = "smtp.gmail.com"
    # # SMTP_PORT = 587 # For STARTTLS
    # # SMTP_PORT = 465 # For SSL
    #
    # # Example for a local debug server (e.g., python -m smtpd -n -c DebuggingServer localhost:1025)
    # # SMTP_SERVER = "localhost"
    # # SMTP_PORT = 1025

    # mock_phrase_details = {
    #     'phrase': 'The only way to do great work is to love what you do.',
    #     'author': 'Steve Jobs',
    #     'location': 'Palo Alto'
    # }
    #
    # if TEST_SENDER_EMAIL != "your_email@example.com": # Basic check before trying
    #     print(f"Attempting to send test email from {TEST_SENDER_EMAIL} to {TEST_RECIPIENT_EMAIL} via {SMTP_SERVER}:{SMTP_PORT}...")
    #     success = send_email(
    #         mock_phrase_details,
    #         TEST_RECIPIENT_EMAIL,
    #         TEST_SENDER_EMAIL,
    #         TEST_SENDER_PASSWORD,
    #         SMTP_SERVER,
    #         SMTP_PORT
    #     )
    #     if success:
    #         print("Test email attempt finished successfully (check recipient inbox).")
    #     else:
    #         print("Test email attempt failed.")
    # else:
    #     print("Please configure test email parameters in src/email_sender.py to run the example.")
    pass
