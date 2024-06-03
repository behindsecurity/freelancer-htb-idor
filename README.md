# Freelancer HTB Proof of Concept

This proof of concept (PoC) script demonstrates the automation of several interactions with the HTB Freelancer CTF website, including account creation, login, and user data extraction using QR code authentication bypass.

## Features

- **Account Creation**: Automatically create a new user account with provided credentials.
- **Login**: Perform a login operation using the created or existing user credentials.
- **QR Code Download and Decode**: Download and decode QR codes to extract authentication tokens.
- **User Data Extraction**: Access and extract user details after successful authentication with the QR code.
- **Error Handling**: Includes robust error handling and logging for each step of the process.

## Requirements

- Python 3.8+
- Libraries: `requests`, `cv2`, `numpy`, `base64`, `sys`, `logging`, `BeautifulSoup`, `pyzbar`

Install the necessary Python libraries using:

```bash
pip install requests opencv-python numpy BeautifulSoup4 pyzbar
```

## Usage

1. Ensure you have Python installed and the required libraries.
2. Download the script to your local machine.
3. Run the script using:

```bash
python3 freelancer_poc.py
```

The script will perform the following operations:
- Create and activate a new user account or use an existing one to log in.
- Attempt to retrieve and decode the QR code for multiple user IDs.
- Extract and save user details for accounts that can be accessed using the decoded QR code.

## Configuration

The script runs without the need for any additional configuration. However, you can change these values in the code as you wish.

- `USERNAME`: Set the username for login or account creation.
- `PASSWORD`: Set the password for login or account creation.
- `QR_CODE_URL`: URL to fetch the QR code for authentication.
- `IMAGE_PATH`: Local path to save the downloaded QR code image.

## Warning

This script is designed for educational purposes and ethical testing only.

## Logging

The script uses Python's built-in logging library to provide detailed logs for each operation, aiding in debugging and tracking the script's execution flow.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
