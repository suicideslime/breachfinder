import requests
from typing import Optional, Dict
from dataclasses import dataclass
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from logger import Logger
from urllib.parse import urlparse
from rate_limiter import RateLimiter
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests_ntlm import HttpNtlmAuth
import json
from config import Config

@dataclass
class Credential:
    url: str
    username: str
    password: str

    @classmethod
    def from_line(cls, line: str) -> Optional['Credential']:
        """Create a Credential object from a line of text in format url|user|pass"""
        try:
            url, username, password = line.strip().split('|')
            return cls(url=url, username=username, password=password)
        except ValueError:
            return None

    def to_line(self) -> str:
        """Convert credential to string format url|user|pass"""
        return f"{self.url}|{self.username}|{self.password}"

class AuthenticationMethod:
    @staticmethod
    def get_auth_handler(method: str, username: str, password: str, params: Dict[str, str]):
        if method == "basic":
            return HTTPBasicAuth(username, password)
        elif method == "digest":
            return HTTPDigestAuth(username, password)
        elif method == "ntlm":
            return HttpNtlmAuth(username, password)
        elif method == "form":
            return None  # Form authentication handled separately
        else:
            raise ValueError(f"Unsupported authentication method: {method}")

    @staticmethod
    def get_form_data(username: str, password: str, params: Dict[str, str]) -> Dict[str, str]:
        form_data = params.copy()
        form_data[params.get('username_field', 'username')] = username
        form_data[params.get('password_field', 'password')] = password
        return form_data

class CredentialChecker:
    def __init__(self, max_retries: int = 3, logger: Optional[Logger] = None, 
                 requests_per_second: int = 2, config: Optional[Config] = None):
        self.session = requests.Session()
        self.logger = logger or Logger("logs/app.log")
        self.rate_limiter = RateLimiter(requests_per_second)
        self.config = config or Config(input_file="")
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Configure proxy if specified
        if config and config.proxy:
            proxies = {
                'http': config.proxy.http,
                'https': config.proxy.https
            }
            if config.proxy.username and config.proxy.password:
                for protocol in ['http', 'https']:
                    if proxies[protocol]:
                        auth = f"{config.proxy.username}:{config.proxy.password}@"
                        proxies[protocol] = proxies[protocol].replace("://", "://" + auth)
            self.session.proxies.update(proxies)

    def check_credential(self, credential: Credential) -> bool:
        """
        Check if a credential is valid by attempting to authenticate against the URL
        Returns True if credential is valid, False otherwise
        """
        try:
            domain = urlparse(credential.url).netloc
            self.rate_limiter.wait(domain)
            
            self.logger.debug(f"Checking credential for URL: {credential.url}")
            
            auth = AuthenticationMethod.get_auth_handler(
                self.config.auth_method,
                credential.username,
                credential.password,
                self.config.auth_params
            )

            if self.config.auth_method == "form":
                form_data = AuthenticationMethod.get_form_data(
                    credential.username,
                    credential.password,
                    self.config.auth_params
                )
                response = self.session.post(
                    credential.url,
                    data=form_data,
                    timeout=self.config.timeout
                )
            else:
                response = self.session.post(
                    credential.url,
                    auth=auth,
                    timeout=self.config.timeout
                )

            # Check for success based on response
            success_indicators = self.config.auth_params.get('success_indicators', [])
            is_valid = False

            if success_indicators:
                for indicator in success_indicators:
                    if indicator in response.text:
                        is_valid = True
                        break
            else:
                is_valid = response.status_code == 200

            if is_valid:
                self.logger.info(f"Valid credential found: {credential.url}")
            return is_valid

        except requests.RequestException as e:
            self.logger.error(f"Request error for {credential.url}: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error for {credential.url}: {str(e)}")
            return False 