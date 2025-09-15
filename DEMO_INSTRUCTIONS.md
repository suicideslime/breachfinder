# White Hat Breach Finder - Demo Instructions

## Overview

The White Hat Breach Finder is a security tool designed to validate login credentials by attempting to authenticate against specified URLs. It helps identify potential security breaches in a controlled and ethical manner.

## Features Demonstrated

1. **Multi-threaded Processing**: Process multiple credentials concurrently
2. **Rate Limiting**: Control request frequency to avoid overwhelming servers
3. **Multiple Authentication Methods**: Support for Basic, Digest, NTLM, and Form-based authentication
4. **Web Interface**: User-friendly web interface for easy credential checking
5. **CLI Interface**: Command-line interface for automation and scripting

## Sample Data

We've created a sample credential file at `data/credentials.txt` with the following content:

```
http://example.com/login|admin|password123
http://testsite.org/auth|user|testpass
https://demo.example.com|demo|demopass
http://localhost:8080/login|testuser|test123
https://secure.example.com|security|securepass
```

## CLI Interface Demo

### Running the Program

To run the CLI version of the program, use the following command:

```bash
python src/main.py -i data/credentials.txt -t 4 --timeout 10
```

### Command Line Options

- `-i, --input`: Input file containing credentials in format `url|user|pass`
- `-t, --threads`: Number of threads to use (default: 4)
- `--timeout`: Request timeout in seconds (default: 10)
- `--rate-limit`: Maximum requests per second per domain (default: 2)

### Expected Output

When running the program, you'll see output similar to:

```
2025-09-15 11:41:02,400 - BreachFinder - INFO - Starting White Hat Breach Finder
2025-09-15 11:41:02,550 - BreachFinder - INFO - Found 5 credentials to check
2025-09-15 11:41:02,557 - BreachFinder - INFO - Starting credential check with 4 threads
Checking credentials: 100%|##########| 5/5 [00:30<00:00,  6.02s/cred]
2025-09-15 11:41:33,678 - BreachFinder - INFO - No valid credentials found
```

Note: Since our sample URLs are not real, the program will show connection errors, which is expected behavior.

## Web Interface Demo

### Running the Web Interface

To run the web interface, use the following command:

```bash
python src/run_web.py
```

This will start a web server on `http://localhost:5000`.

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. You'll see a web form with the following fields:
   - **Credentials File**: Upload your credentials file
   - **Number of Threads**: Set the number of concurrent threads (default: 4)
   - **Rate Limit**: Set requests per second (default: 2)
3. Click "Start Check" to begin processing
4. The interface will show progress and results in real-time

### Web Interface Features

- Real-time progress bar showing completion status
- Statistics dashboard showing total credentials, valid credentials, and completion rate
- Results table displaying valid credentials
- Download button for saving results

## How It Works

1. **File Reading**: The program reads credentials from a text file in the format `url|user|pass`
2. **Queue Processing**: Credentials are placed in a queue for processing
3. **Multi-threading**: Multiple threads process credentials concurrently
4. **Authentication**: Each credential is tested against its URL
5. **Rate Limiting**: Requests are throttled to avoid overwhelming servers
6. **Results**: Valid credentials are saved to an output file

## Security Considerations

- This tool is intended for authorized security testing only
- Ensure you have proper permissions before testing any systems
- Use responsibly and ethically
- The tool includes rate limiting to prevent server overload

## Troubleshooting

- If you encounter connection errors, ensure the URLs in your credentials file are accessible
- Adjust the number of threads based on your system's capabilities
- Increase timeout values for slow-loading websites