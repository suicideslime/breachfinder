# White Hat Breach Finder - Uni Project Submission

## Project Overview

This submission includes a complete implementation of the White Hat Breach Finder, a security tool designed to validate login credentials ethically and responsibly.

## Components Included

1. **Core Application** - The main credential checking tool with both CLI and web interfaces
2. **Documentation** - Comprehensive guides for installation and usage
3. **Sample Data** - Example credential files for demonstration
4. **Test Suite** - Unit tests to verify functionality

## How to Run the Application

### Web Interface (Easiest Method)
1. Open terminal in the project directory
2. Run: `python src/run_web.py`
3. Open browser to: http://localhost:5000
4. Upload credentials file and start checking

### Command Line Interface
1. Open terminal in the project directory
2. Run: `python src/main.py -i data/credentials.txt -t 4`
3. View results in `data/valid.txt`

## Key Features Demonstrated

- Multi-threaded processing for faster checking
- Rate limiting to prevent server overload
- Progress tracking and real-time updates
- Both web and command-line interfaces
- Comprehensive error handling and logging

## Sample Credential File

A sample credential file is provided at `data/credentials.txt` with the following format:
```
url|username|password
```

Example:
```
http://example.com/login|admin|password123
```

## Documentation

- `README.md` - Main project documentation
- `DEMO_INSTRUCTIONS.md` - Step-by-step usage guide
- `WEB_INTERFACE_DEMO.md` - Web interface walkthrough

## Technical Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`
- Internet connection for testing credentials

## Security Notice

This tool is for educational and authorized security testing only. Always ensure you have permission before testing any system.

## Files in This Submission

```
breachfinder/
├── README.md                 # Main documentation
├── UNI_PROJECT_SUMMARY.md    # This file
├── DEMO_INSTRUCTIONS.md      # Usage instructions
├── WEB_INTERFACE_DEMO.md     # Web interface guide
├── requirements.txt          # Python dependencies
├── data/
│   ├── credentials.txt       # Sample input file
│   └── valid.txt             # Output file (created during run)
├── src/
│   ├── main.py              # CLI entry point
│   ├── run_web.py           # Web interface entry point
│   └── [other source files]  # Core application modules
└── logs/
    └── app.log              # Log file (created during run)
```

## How to Demonstrate This Project

1. Show the web interface by running `python src/run_web.py`
2. Demonstrate the CLI by running `python src/main.py -i data/credentials.txt`
3. Explain the multi-threading and rate limiting features
4. Show the logging and output files

## Troubleshooting

If you encounter any issues:
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check that Python 3.7+ is installed
3. Verify internet connectivity
4. Check logs in `logs/app.log` for detailed error information

## Academic Integrity Note

This tool is designed for educational purposes and ethical security testing. It should only be used on systems you own or have explicit permission to test.