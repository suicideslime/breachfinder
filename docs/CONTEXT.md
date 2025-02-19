# White Hat Breach Finder Application

## Overview

The **White Hat Breach Finder** is a Python-based application designed to help users identify potential security breaches by analyzing login credentials stored in a `.txt` file. The application validates these credentials by attempting to authenticate against specified URLs. Valid credentials are saved in a separate file for further investigation. The application supports multi-threading, allowing users to specify the number of threads for concurrent processing.

## Features

- **File Upload**: Users can upload a `.txt` file containing login credentials in the format `url|user|pass`.
- **Credential Validation**: The application checks the validity of credentials by authenticating against the specified URLs.
- **Multi-threading**: Users can specify the number of threads for concurrent processing.
- **Output File**: Valid credentials are saved in a file named `valid.txt`.
- **User-Friendly Interface**: The application prompts users for the file path and the number of threads, making it easy to use.

## Application Flow

1. **Initialization**: 
   - The application displays a welcome message and prompts the user to enter the file path of the `.txt` file containing the credentials.

2. **File Reading**: 
   - The application reads the `.txt` file line by line, expecting each line to be in the format `url|user|pass`.

3. **Credential Validation**: 
   - For each line, the application extracts the URL, username, and password, then attempts to authenticate against the URL using the provided credentials. Successful authentications are considered valid.

4. **Multi-threading**: 
   - Users specify the number of threads for concurrent processing, allowing the application to divide the workload among the specified threads to speed up validation.

5. **Saving Valid Credentials**: 
   - Valid credentials are saved in a file named `valid.txt` in the same directory as the script, maintaining the format `url|user|pass`.

6. **Completion**: 
   - After processing all credentials, the application displays a completion message and exits.

## Database Schema

The application can utilize a simple database schema to store valid credentials and logs. Below is a suggested schema:

### Tables

1. **Users**
   - `id` (INTEGER, Primary Key, Auto Increment)
   - `url` (TEXT, NOT NULL)
   - `username` (TEXT, NOT NULL)
   - `password` (TEXT, NOT NULL)
   - `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

2. **Logs**
   - `id` (INTEGER, Primary Key, Auto Increment)
   - `user_id` (INTEGER, Foreign Key referencing Users(id))
   - `status` (TEXT, NOT NULL)  // e.g., 'valid', 'invalid', 'error'
   - `timestamp` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

## Optimal Folder Structure

To maintain a clean and organized project, consider the following folder structure:

```
white_hat_breach_finder/
│
├── src/                     # Source code directory
│   ├── main.py              # Main application script
│   ├── credential_checker.py # Module for credential validation
│   ├── worker.py            # Module for worker threads
│   └── utils.py             # Utility functions
│
├── data/                    # Data directory
│   ├── valid.txt            # Output file for valid credentials
│   └── credentials.txt      # Input file for credentials
│
├── logs/                    # Log files directory
│   └── app.log              # Application log file
│
├── tests/                   # Test directory
│   ├── test_main.py         # Tests for main application
│   └── test_utils.py        # Tests for utility functions
│
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Code Structure

### Main Script

```python
import threading
import requests
from queue import Queue

# Function to check the validity of credentials
def check_credential(url, user, passw, valid_queue):
    try:
        # Example of a simple POST request for authentication
        response = requests.post(url, data={'username': user, 'password': passw})
        if response.status_code == 200:
            valid_queue.put(f"{url}|{user}|{passw}")
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")

# Worker function to process the queue
def worker(cred_queue, valid_queue):
    while not cred_queue.empty():
        url, user, passw = cred_queue.get()
        check_credential(url, user, passw, valid_queue)
        cred_queue.task_done()

# Main function
def main():
    file_path = input("Insert the file path: ")
    num_threads = int(input("Set the number of threads: "))

    cred_queue = Queue()
    valid_queue = Queue()

    # Read the file and populate the queue
    with open(file_path, 'r') as file:
        for line in file:
            url, user, passw = line.strip().split('|')
            cred_queue.put((url, user, passw))

    # Create and start threads
    for _ in range(num_threads):
        threading.Thread(target=worker, args=(cred_queue, valid_queue)).start()

    # Wait for all threads to finish
    cred_queue.join()

    # Save valid credentials to valid.txt
    with open('valid.txt', 'w') as valid_file:
        while not valid_queue.empty():
            valid_file.write(valid_queue.get() + "\n")

    print("Process completed. Valid credentials saved in valid.txt.")

if __name__ == "__main__":
    main()
```

### Explanation of the Code

- **check_credential Function**: Validates credentials by attempting to authenticate against the URL. If successful, it adds the credentials to the `valid_queue`.
- **worker Function**: Processes credentials from the `cred_queue`, calling `check_credential` for each set and marking the task as done once processed.
- **main Function**: Initializes queues, reads the input file, populates the `cred_queue`, creates and starts threads, and saves valid credentials to `valid.txt` after processing.

## Usage Instructions

1. **Prepare the Input File**: Create a `.txt` file with credentials in the format `url|user|pass`.
2. **Run the Script**: Execute the script using Python. When prompted, enter the file path of the `.txt` file and specify the number of threads to use.
3. **Review the Output**: After completion, check the `valid.txt` file for valid credentials.

## Conclusion

The **White Hat Breach Finder** is a powerful tool for identifying potential security breaches by validating login credentials. Its multi-threaded design ensures efficient processing, making it suitable for large datasets. By following the structured flow and code provided, cybersecurity professionals can easily implement and customize this application to meet their specific needs.

