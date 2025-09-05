
import argparse
import json
import sys
import os
from datetime import datetime
from colorama import Fore, Style, init

from modules.shodan_module import ShodanModule
from modules.crtsh_module import CrtshModule
from modules.maigret_module import MaigretModule
from modules.holehe_module import HoleheModule
from modules.wayback_module import WaybackModule
from modules.whois_module import WhoisModule
from modules.dig_module import DigModule
from modules.ping_module import PingModule
from utils.output_handler import OutputHandler
from utils.config_loader import ConfigLoader

init(autoreset=True)

class AAOT:

    def __init__(self):
        self.modules = {}
        self.results = {}
        self.output_handler = OutputHandler()
        self.config = ConfigLoader()

    def initialize_modules(self):
        try:
            if self.config.has_api_key('shodan'):
                self.modules['shodan'] = ShodanModule(self.config)

            self.modules['crtsh'] = CrtshModule(self.config)

            self.modules['maigret'] = MaigretModule(self.config)
            self.modules['holehe'] = HoleheModule(self.config)
            self.modules['wayback'] = WaybackModule(self.config)
            self.modules['whois'] = WhoisModule(self.config)
            self.modules['dig'] = DigModule(self.config)
            self.modules['ping'] = PingModule(self.config)

        except (ValueError, RuntimeError, ImportError) as e:
            self.output_handler.error(f"Failed to initialize modules: {e}")
            return False

        return True

    def run_module(self, module_name, target):
        if module_name not in self.modules:
            self.output_handler.warning(f"Module {module_name} not available or configured")
            return None

        try:
            self.output_handler.info(f"Running {module_name} module...")
            result = self.modules[module_name].run(target)
            return result
        except RuntimeError as e:
            self.output_handler.error(f"Error in {module_name} module: {e}")
            return None

    def run_all(self, target, module_list=None):
        modules_to_run = module_list if module_list else self.modules.keys()

        for module_name in modules_to_run:
            result = self.run_module(module_name, target)
            if result:
                self.results[module_name] = result

        return self.results

def main():
    parser = argparse.ArgumentParser(description="AAOT - Advanced OSINT Tool")
    parser.add_argument("target", help="Target domain, IP, or email address")
    parser.add_argument("-m", "--modules", help="Comma-separated list of modules to run")
    parser.add_argument("-o", "--output", help="Output file name", default="aaot_results")
    parser.add_argument("-f", "--format", help="Output format (json, txt, html)", default="json")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-c", "--config", help="Path to config directory", default="config")

    args = parser.parse_args()

    tool = AAOT()

    try:
        tool.config.load(args.config)
    except (FileNotFoundError, ValueError) as e:
        print(f"{Fore.RED}[!] Failed to load configuration: {e}")
        sys.exit(1)

    if not tool.initialize_modules():
        print(f"{Fore.RED}[!] Failed to initialize modules. Check your API configuration.")
        sys.exit(1)

    if not tool.modules:
        print(f"{Fore.YELLOW}[!] No modules configured. Please check your API keys.")
        sys.exit(1)

    modules_to_run = None
    if args.modules:
        modules_to_run = [m.strip() for m in args.modules.split(",")]

    print(f"{Fore.CYAN}[*] Starting AAOT scan for: {args.target}")
    print(f"{Fore.CYAN}[*] Available modules: {', '.join(tool.modules.keys())}")

    results = tool.run_all(args.target, modules_to_run)

    if results:
        output_file = tool.output_handler.save_results(
            results,
            args.output,
            args.format
        )
        print(f"{Fore.GREEN}[+] Scan completed. Results saved to: {output_file}")
    else:
        print(f"{Fore.YELLOW}[-] No results obtained from the scan.")

if __name__ == "__main__":
    main()
