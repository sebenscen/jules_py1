# Daily Inspirational Emailer

## Description
This project automatically sends a daily inspirational phrase via email. It uses the Google Gemini API to generate unique phrases, including the author and their primary location (when available).

## Features
*   Daily automated email delivery.
*   AI-generated inspirational phrases, authors, and locations using Google Gemini.
*   Includes the phrase, its author, and the author's primary location (if available).
*   Configurable sender and recipient email settings via environment variables.

## Prerequisites
*   Python 3.7+
*   Access to an SMTP server (e.g., Gmail, Outlook, or a private mail server).
*   A Google API Key for the Gemini API.

## Setup & Configuration

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```
    (Replace `<repository_url>` with the actual URL of this repository)

2.  **Navigate to the project directory:**
    ```bash
    cd <project_directory>
    ```
    (Replace `<project_directory>` with the name of the cloned folder)

3.  **Create a Python virtual environment:**
    A virtual environment is recommended to manage project dependencies.
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies:**
    (Note: `requirements.txt` will be created in a subsequent step. For now, this is a placeholder for when it's added.)
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Variables:**
    The application is configured using environment variables. These can be set directly in your operating system or, more conveniently, by creating a `.env` file in the root of the project directory.

    Create a file named `.env` in the project root and add the following content, replacing the placeholder values with your actual credentials:
    ```env
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    RECIPIENT_EMAIL="your_recipient_email@example.com"
    SENDER_EMAIL="your_sending_email@example.com"
    SENDER_PASSWORD="your_sender_email_password_or_app_password"
    SMTP_SERVER="smtp.example.com"
    SMTP_PORT="587" # Use 587 for TLS/STARTTLS (e.g., Gmail), or 465 for SSL.
    ```

    *   **Getting a `GOOGLE_API_KEY`:**
        1.  Go to [Google AI Studio](https://aistudio.google.com/).
        2.  Sign in with your Google account.
        3.  Click on "Get API key" and create a new API key. Ensure the Gemini API (or its equivalent, like "Generative Language API") is enabled for your Google Cloud project associated with the key.
    *   **Email Provider Settings (e.g., Gmail):**
        *   If you are using Gmail and have 2-Factor Authentication (2FA) enabled, you'll need to create an "App Password" for this application. Go to your Google Account settings -> Security -> App passwords.
        *   For other email providers, consult their documentation for SMTP server details (server address, port) and authentication requirements (e.g., if they require app-specific passwords).

## Running the Application

To send an email manually (ensure your virtual environment is activated and the `.env` file is correctly configured):
```bash
python main.py
```

## Running Tests

To run the automated unit tests (ensure your virtual environment is activated):
```bash
python -m unittest discover tests
```
This command will discover and run all tests located in the `tests/` directory.

## Scheduling Daily Execution

To automate the daily sending of emails, you can use a task scheduler.

*   **Cron (Linux/macOS):**
    Open your crontab for editing:
    ```bash
    crontab -e
    ```
    Add a line similar to the following, adjusting the paths to match your project setup. This example runs the script daily at 9:00 AM:
    ```cron
    0 9 * * * /path/to/your/project/venv/bin/python /path/to/your/project/main.py >> /path/to/your/project/cron.log 2>&1
    ```
    *   Replace `/path/to/your/project/venv/bin/python` with the absolute path to the Python interpreter inside your project's virtual environment.
    *   Replace `/path/to/your/project/main.py` with the absolute path to your project's `main.py` script.
    *   The `>> /path/to/your/project/cron.log 2>&1` part redirects standard output and standard error to a log file, which is useful for debugging.

*   **Task Scheduler (Windows):**
    1.  Open Task Scheduler.
    2.  Click "Create Basic Task..."
    3.  Name the task (e.g., "Daily Inspirational Email").
    4.  Set the **Trigger** (e.g., Daily, at your desired time like 9:00 AM).
    5.  For the **Action**, select "Start a program."
    6.  In "Program/script," browse to or type the full path to the `python.exe` interpreter within your project's virtual environment (e.g., `C:\path\to\your\project\venv\Scripts\python.exe`).
    7.  In "Add arguments (optional)," enter `main.py`.
    8.  In "Start in (optional)," enter the full path to your project's root directory (e.g., `C:\path\to\your\project\`).
    9.  Review and finish the setup.

## Project Structure
```
.
├── main.py                 # Main script to run the application
├── src/                    # Core application logic
│   ├── __init__.py         # Makes 'src' a Python package
│   ├── phrase_generator.py # Module for generating inspirational phrases
│   └── email_sender.py     # Module for handling email sending
├── config/                 # Configuration files
│   ├── __init__.py         # Makes 'config' a Python package
│   └── settings.py         # Loads and provides configuration from environment variables
├── tests/                  # Unit tests
│   ├── __init__.py         # Makes 'tests' a Python package
│   ├── test_phrase_generator.py
│   └── test_email_sender.py
├── venv/                   # Python virtual environment (typically not committed)
├── .env                    # (User-created and gitignored) For storing environment variables locally
├── .gitignore              # Specifies intentionally untracked files that Git should ignore
└── README.md               # This file
└── requirements.txt        # Project dependencies (to be created)
```

---
This README provides a comprehensive guide for users to set up, configure, and run the Daily Inspirational Emailer.
