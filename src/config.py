import os
from dataclasses import dataclass, field
from typing import Optional, Dict
import json

@dataclass
class ProxyConfig:
    http: Optional[str] = None
    https: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

@dataclass
class Config:
    input_file: str
    output_file: str = "data/valid.txt"
    num_threads: int = 600
    max_retries: int = 3
    timeout: int = 10
    log_file: str = "logs/app.log"
    log_level: str = "INFO"
    requests_per_second: int = 2  # New field for rate limiting
    proxy: Optional[ProxyConfig] = None
    auth_method: str = "ntlm"  # basic, form, digest, ntlm
    auth_params: Dict[str, str] = field(default_factory=dict)
    rage: bool = False
    
    @classmethod
    def load_from_file(cls, config_path: str) -> Optional['Config']:
        """Load configuration from a JSON file"""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                return cls(**config_data)
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return None

    def save_to_file(self, config_path: str) -> bool:
        """Save current configuration to a JSON file"""
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(self.__dict__, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            return False 