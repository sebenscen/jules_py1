import unittest
from unittest.mock import patch, MagicMock, call
import datetime
from email.mime.text import MIMEText # Though not directly instantiated, useful for type hints or reference

from src.email_sender import send_email

class TestEmailSender(unittest.TestCase):

    def setUp(self):
        self.phrase_details_full = {
            'phrase': 'Be the change you wish to see.',
            'author': 'Mahatma Gandhi',
            'location': 'India'
        }
        self.phrase_details_no_loc = {
            'phrase': 'Simplicity is the ultimate sophistication.',
            'author': 'Leonardo da Vinci',
            'location': None
        }
        self.recipient_email = "recipient@example.com"
        self.sender_email = "sender@example.com"
        self.sender_password = "password123"
        self.smtp_server_address = "smtp.example.com"
        
        # Mock datetime to control the date in the email body
        self.mock_date = datetime.date(2023, 10, 26)
        self.patcher = patch('src.email_sender.datetime.date')
        self.mock_datetime_date = self.patcher.start()
        self.mock_datetime_date.today.return_value = self.mock_date

    def tearDown(self):
        self.patcher.stop()

    @patch('src.email_sender.smtplib.SMTP_SSL')
    def test_send_email_success_ssl(self, MockSMTP_SSL):
        mock_server_instance = MockSMTP_SSL.return_value
        
        result = send_email(
            self.phrase_details_full,
            self.recipient_email,
            self.sender_email,
            self.sender_password,
            self.smtp_server_address,
            465  # SSL port
        )

        self.assertTrue(result)
        MockSMTP_SSL.assert_called_once_with(self.smtp_server_address, 465)
        mock_server_instance.login.assert_called_once_with(self.sender_email, self.sender_password)
        
        # Check email content
        self.assertEqual(mock_server_instance.sendmail.call_count, 1)
        args, _ = mock_server_instance.sendmail.call_args
        sent_from, sent_to_list, msg_string = args
        
        self.assertEqual(sent_from, self.sender_email)
        self.assertIn(self.recipient_email, sent_to_list) # sendmail takes a list of recipients
        
        # Parse the msg_string to check headers and body
        # For simplicity, we'll check substrings. A more robust way is to parse with email.parser
        self.assertIn(f"Subject: Your Daily Inspirational Phrase", msg_string)
        self.assertIn(f"From: {self.sender_email}", msg_string)
        self.assertIn(f"To: {self.recipient_email}", msg_string)
        
        expected_body_part_phrase = '"Be the change you wish to see."'
        expected_body_part_author = "- Mahatma Gandhi"
        expected_body_part_location = "(Location: India)"
        expected_body_part_date = "Today's inspirational phrase (2023-10-26):"
        
        self.assertIn(expected_body_part_date, msg_string)
        self.assertIn(expected_body_part_phrase, msg_string)
        self.assertIn(expected_body_part_author, msg_string)
        self.assertIn(expected_body_part_location, msg_string)
        
        mock_server_instance.quit.assert_called_once()

    @patch('src.email_sender.smtplib.SMTP')
    def test_send_email_success_tls(self, MockSMTP):
        mock_server_instance = MockSMTP.return_value
        
        result = send_email(
            self.phrase_details_full,
            self.recipient_email,
            self.sender_email,
            self.sender_password,
            self.smtp_server_address,
            587  # TLS port
        )

        self.assertTrue(result)
        MockSMTP.assert_called_once_with(self.smtp_server_address, 587)
        self.assertEqual(mock_server_instance.ehlo.call_count, 2) # Before and after starttls
        mock_server_instance.starttls.assert_called_once()
        mock_server_instance.login.assert_called_once_with(self.sender_email, self.sender_password)
        
        self.assertEqual(mock_server_instance.sendmail.call_count, 1)
        args, _ = mock_server_instance.sendmail.call_args
        _, _, msg_string = args # Only need msg_string for content check here
        
        expected_body_part_phrase = '"Be the change you wish to see."'
        expected_body_part_author = "- Mahatma Gandhi"
        expected_body_part_location = "(Location: India)"
        expected_body_part_date = "Today's inspirational phrase (2023-10-26):"

        self.assertIn(expected_body_part_date, msg_string)
        self.assertIn(expected_body_part_phrase, msg_string)
        self.assertIn(expected_body_part_author, msg_string)
        self.assertIn(expected_body_part_location, msg_string)
        
        mock_server_instance.quit.assert_called_once()

    @patch('src.email_sender.smtplib.SMTP_SSL') # Assuming SSL for this specific test
    def test_send_email_missing_location(self, MockSMTP_SSL):
        mock_server_instance = MockSMTP_SSL.return_value
        
        result = send_email(
            self.phrase_details_no_loc, # Using details with no location
            self.recipient_email,
            self.sender_email,
            self.sender_password,
            self.smtp_server_address,
            465
        )
        self.assertTrue(result)
        
        args, _ = mock_server_instance.sendmail.call_args
        _, _, msg_string = args
        
        expected_body_part_phrase = '"Simplicity is the ultimate sophistication."'
        expected_body_part_author = "- Leonardo da Vinci"
        unwanted_body_part_location = "(Location:" # Check that "Location:" line is not present

        self.assertIn(expected_body_part_phrase, msg_string)
        self.assertIn(expected_body_part_author, msg_string)
        self.assertNotIn(unwanted_body_part_location, msg_string)

    @patch('src.email_sender.smtplib.SMTP_SSL')
    def test_send_email_login_failure(self, MockSMTP_SSL):
        mock_server_instance = MockSMTP_SSL.return_value
        mock_server_instance.login.side_effect = smtplib.SMTPAuthenticationError(535, b"Authentication credentials invalid")
        
        result = send_email(
            self.phrase_details_full,
            self.recipient_email,
            self.sender_email,
            self.sender_password,
            self.smtp_server_address,
            465
        )
        self.assertFalse(result)
        mock_server_instance.quit.assert_not_called() # Should not be called if login fails

    @patch('src.email_sender.smtplib.SMTP_SSL')
    def test_send_email_sendmail_failure(self, MockSMTP_SSL):
        mock_server_instance = MockSMTP_SSL.return_value
        mock_server_instance.sendmail.side_effect = smtplib.SMTPException("Failed to send email")
        
        result = send_email(
            self.phrase_details_full,
            self.recipient_email,
            self.sender_email,
            self.sender_password,
            self.smtp_server_address,
            465
        )
        self.assertFalse(result)
        mock_server_instance.quit.assert_called_once() # Quit should still be called

    @patch('src.email_sender.smtplib.SMTP')
    def test_send_email_connect_failure_tls(self, MockSMTP):
        MockSMTP.side_effect = smtplib.SMTPConnectError(500, "Connection timed out")

        result = send_email(
            self.phrase_details_full,
            self.recipient_email,
            self.sender_email,
            self.sender_password,
            self.smtp_server_address,
            587 # TLS port
        )
        self.assertFalse(result)

    @patch('src.email_sender.smtplib.SMTP_SSL')
    def test_send_email_connect_failure_ssl(self, MockSMTP_SSL):
        MockSMTP_SSL.side_effect = smtplib.SMTPConnectError(500, "Connection timed out")

        result = send_email(
            self.phrase_details_full,
            self.recipient_email,
            self.sender_email,
            self.sender_password,
            self.smtp_server_address,
            465 # SSL port
        )
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
