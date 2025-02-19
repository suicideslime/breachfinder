import argparse
from typing import Optional
from config import Config, ProxyConfig
import json

class CLI:
    @staticmethod
    def parse_args() -> Config:
        parser = argparse.ArgumentParser(
            description="White Hat Breach Finder - Check credentials against URLs",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # Required arguments
        parser.add_argument(
            "-i", "--input",
            required=True,
            help="Input file containing credentials in format url|user|pass"
        )

        # Optional arguments
        parser.add_argument(
            "-o", "--output",
            default="data/valid.txt",
            help="Output file for valid credentials"
        )
        parser.add_argument(
            "-t", "--threads",
            type=int,
            default=4,
            help="Number of threads to use"
        )
        parser.add_argument(
            "-r", "--retries",
            type=int,
            default=3,
            help="Maximum number of retries for failed requests"
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=10,
            help="Request timeout in seconds"
        )
        parser.add_argument(
            "--log-file",
            default="logs/app.log",
            help="Log file path"
        )
        parser.add_argument(
            "--log-level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            default="INFO",
            help="Logging level"
        )
        parser.add_argument(
            "--rate-limit",
            type=int,
            default=2,
            help="Maximum requests per second per domain"
        )
        parser.add_argument(
            "--save-config",
            help="Save configuration to specified file"
        )
        parser.add_argument(
            "--load-config",
            help="Load configuration from specified file"
        )

        # Proxy arguments
        proxy_group = parser.add_argument_group('Proxy Configuration')
        proxy_group.add_argument(
            "--proxy-http",
            help="HTTP proxy URL (e.g., http://proxy.example.com:8080)"
        )
        proxy_group.add_argument(
            "--proxy-https",
            help="HTTPS proxy URL"
        )
        proxy_group.add_argument(
            "--proxy-user",
            help="Proxy authentication username"
        )
        proxy_group.add_argument(
            "--proxy-pass",
            help="Proxy authentication password"
        )

        # Authentication arguments
        auth_group = parser.add_argument_group('Authentication Configuration')
        auth_group.add_argument(
            "--auth-method",
            choices=["basic", "form", "digest", "ntlm"],
            default="basic",
            help="Authentication method to use"
        )
        auth_group.add_argument(
            "--auth-params",
            type=json.loads,
            default="{}",
            help="JSON string of additional authentication parameters"
        )

        parser.add_argument(
            "--rage",
            action="store_true",
            help="Enable rage mode to dynamically adjust threads from 100 to 600"
        )

        args = parser.parse_args()

        # Load config from file if specified
        if args.load_config:
            config = Config.load_from_file(args.load_config)
            if not config:
                parser.error(f"Failed to load config from {args.load_config}")
            return config

        # Create proxy config if proxy settings provided
        proxy_config = None
        if args.proxy_http or args.proxy_https:
            proxy_config = ProxyConfig(
                http=args.proxy_http,
                https=args.proxy_https,
                username=args.proxy_user,
                password=args.proxy_pass
            )

        # Create config from command line arguments
        config = Config(
            input_file=args.input,
            output_file=args.output,
            num_threads=args.threads,
            max_retries=args.retries,
            timeout=args.timeout,
            log_file=args.log_file,
            log_level=args.log_level,
            requests_per_second=args.rate_limit,
            proxy=proxy_config,
            auth_method=args.auth_method,
            auth_params=args.auth_params,
            rage=args.rage
        )

        # Save config if requested
        if args.save_config:
            if not config.save_to_file(args.save_config):
                parser.error(f"Failed to save config to {args.save_config}")

        return config 