# Password Strength Checker

A Python command-line application that evaluates password characteristics, assigns a heuristic strength score, and provides actionable feedback.

## Features

- Analyzes password length and character categories.
- Calculates a score from 0 to 6.
- Classifies passwords as Weak, Medium, or Strong.
- Checks an embedded local list of common passwords.
- Generates recommendations based on detected characteristics.
- Hides password input in the terminal using Python's `getpass`.
- Includes automated tests with `pytest`.

## Technologies

- Python
- pytest
- Git and GitHub

## Project Structure

```text
PasswordStrengthChecker/
├── password_checker.py
├── tests/
│   └── test_password_checker.py
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or later
- pip

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd PasswordStrengthChecker
```

No third-party packages are required to run the application. Install pytest to execute the test suite:

```bash
python -m pip install pytest
```

## Usage

Run the application:

```bash
python password_checker.py
```

Enter a fictional test password when prompted. The application displays its classification, score, detected characteristics, and recommendations.

## Running Tests

Execute the automated test suite:

```bash
python -m pytest -v
```

## How It Works

1. **Input validation:** Rejects empty or whitespace-only input and non-string values.
2. **Feature extraction:** Checks length, lowercase letters, uppercase letters, digits, and symbols.
3. **Scoring:** Assigns points based on length and detected character categories.
4. **Classification:** Applies the configured rules to determine the strength label.
5. **Common-password check:** Compares the password against a small local denylist.
6. **Recommendations:** Generates feedback based on the evaluation results.

## Security Limitations

This project is an educational demonstration, not a complete password-security auditing solution.

- The score is a simple heuristic, not a calibrated measure of resistance to guessing.
- The common-password list is small and cannot identify every weak or compromised password.
- The application does not query breach databases or verify whether a password has been exposed.
- Character variety alone does not guarantee a secure password.
- Passwords should never be reused across accounts.

## Future Improvements

- Improve password-guessability analysis.
- Expand the automated test suite with boundary and edge cases.
- Add configurable scoring policies.
- Introduce a graphical or web interface.
- Add optional, privacy-preserving breach-checking functionality.

## Learning Objectives

This project demonstrates Python functions, string handling, conditional logic, input validation, automated testing, modular design, and fundamental password-security concepts.
