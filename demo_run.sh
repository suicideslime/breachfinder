#!/bin/bash
# Demo script for White Hat Breach Finder

echo "White Hat Breach Finder - Demo Script"
echo "====================================="
echo

echo "1. Starting Web Interface Demo"
echo "   Run: python src/run_web.py"
echo "   Then visit http://localhost:5000 in your browser"
echo

echo "2. Starting CLI Interface Demo"
echo "   Run: python src/main.py -i data/credentials.txt -t 2"
echo

echo "3. View Results"
echo "   Valid credentials will be saved to: data/valid.txt"
echo "   Logs can be found at: logs/app.log"
echo

echo "Documentation:"
echo "  - README.md: Main documentation"
echo "  - DEMO_INSTRUCTIONS.md: Step-by-step guide"
echo "  - WEB_INTERFACE_DEMO.md: Web interface walkthrough"
echo

echo "Sample credential file format (data/credentials.txt):"
echo "  url|username|password"
echo "  http://example.com/login|admin|password123"
echo

echo "To run the web interface now, use: python src/run_web.py"
echo "To run the CLI interface now, use: python src/main.py -i data/credentials.txt -t 2"