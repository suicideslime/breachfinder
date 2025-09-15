# White Hat Breach Finder

## What is this tool?

The White Hat Breach Finder is a security tool that helps you check if login credentials (username/password combinations) are valid by testing them against websites. It's designed for ethical security testing - to help you identify weak passwords in your own systems or with proper authorization.

## How it works

1. You create a file with login credentials in the format: `website_url|username|password`
2. The tool tries to log in to each website using the provided credentials
3. Valid logins are saved to a results file
4. You can see progress in real-time

## Prerequisites

Before using this tool, make sure you have:
- Python 3.7 or higher installed
- Internet connection
- Proper authorization to test the websites in your credentials file

## Installation

1. Download or clone this repository
2. Open a terminal/command prompt in the project folder
3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Using the Web Interface (Recommended for Beginners)

The web interface is the easiest way to use this tool:

1. Start the web server:
   ```
   python src/run_web.py
   ```

2. Open your browser and go to: http://localhost:5000

3. You'll see a simple form where you can:
   - Upload your credentials file
   - Set the number of threads (concurrent tests)
   - Set rate limits (requests per second)

4. Click "Start Check" and watch the progress

## Using the Command Line Interface

If you prefer the command line:

1. Prepare your credentials file with entries like:
   ```
   http://example.com/login|admin|password123
   https://testsite.org/auth|user|testpass
   ```

2. Run the tool:
   ```
   python src/main.py -i data/credentials.txt -t 4
   ```

### Command Line Options

- `-i, --input FILE` - Input file with credentials (required)
- `-t, --threads N` - Number of concurrent threads (default: 4)
- `--timeout SECONDS` - Request timeout (default: 10)
- `-o, --output FILE` - Output file for valid credentials (default: data/valid.txt)
- `--rate-limit N` - Requests per second limit (default: 2)

Example with more options:
```
python src/main.py -i data/credentials.txt -t 8 --timeout 15 --rate-limit 3
```

## Understanding the Results

- Valid credentials are saved to `data/valid.txt`
- Logs are saved to `logs/app.log`
- Progress is shown in the terminal or web interface

## Security Considerations

⚠️ **Important**: Only use this tool on:
- Systems you own
- Systems you have explicit permission to test
- Test environments, not production systems

The tool includes safeguards like rate limiting to prevent overwhelming servers.

## File Formats

### Credentials File Format
Create a text file with one credential per line:
```
url|username|password
```

Example:
```
http://example.com/login|admin|password123
https://testsite.org/auth|user|testpass
```

### Valid Credentials Output
Valid credentials are saved in the same format:
```
http://example.com/login|admin|password123
```

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Run: `pip install -r requirements.txt`

2. **Connection errors**
   - Check if the URLs in your credentials file are accessible
   - Verify your internet connection

3. **Permission errors**
   - Make sure you have write permissions in the project folder

4. **Slow performance**
   - Reduce the number of threads
   - Increase timeout values for slow websites

### Getting Help

If you encounter issues:
1. Check the logs in `logs/app.log`
2. Ensure you're using Python 3.7+
3. Verify all dependencies are installed

## Example Workflow

1. Create `data/credentials.txt`:
   ```
   http://localhost:8080/login|admin|admin123
   http://testsite.local/auth|user|password
   ```

2. Run the web interface:
   ```
   python src/run_web.py
   ```

3. Visit http://localhost:5000 in your browser

4. Upload your credentials file

5. Click "Start Check"

6. View results in your browser and in `data/valid.txt`

## Contributing

This is an educational tool. Feel free to:
- Report issues
- Suggest improvements
- Add new authentication methods
- Improve the web interface

## License

This tool is for educational purposes. Use responsibly and ethically.
