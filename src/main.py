from credential_checker import Credential
from worker import CredentialWorker
from logger import Logger
from cli import CLI
import os
import sys

def main():
    # Get configuration from command line
    config = CLI.parse_args()
    
    # Initialize logger
    logger = Logger(config.log_file, config.log_level)
    logger.info("Starting White Hat Breach Finder")
    
    if config.rage:
        logger.info("Rage mode enabled")

    # Initialize worker
    worker = CredentialWorker(config)
    credentials = []

    try:
        logger.info(f"Reading credentials from {config.input_file}")
        with open(config.input_file, 'r') as file:
            for line in file:
                credential = Credential.from_line(line)
                if credential:
                    credentials.append(credential)
        
        if not credentials:
            logger.warning("No valid credentials found in file")
            return

        logger.info(f"Found {len(credentials)} credentials to check")
        logger.info(f"Starting credential check with {config.num_threads} threads")

        valid_credentials = worker.process_credentials(credentials)
    
        if valid_credentials:
            os.makedirs(os.path.dirname(config.output_file), exist_ok=True)
            with open(config.output_file, 'w') as valid_file:
                for credential in valid_credentials:
                    valid_file.write(credential.to_line() + '\n')
            logger.info(f"Found {len(valid_credentials)} valid credentials. Saved to {config.output_file}")
        else:
            logger.info("No valid credentials found")
            
    except FileNotFoundError:
        logger.error(f"File not found: {config.input_file}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Stopping...")
        worker.stop_flag.set()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 