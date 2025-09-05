# AAOT - Advanced OSINT Tool

## Overview

AAOT (Advanced OSINT Tool) is a comprehensive open-source intelligence gathering tool designed for security researchers, penetration testers, and cybersecurity professionals. It aggregates data from multiple free OSINT sources to provide detailed information about domains, IPs, and email addresses.


## Features

- **Multi-Source Intelligence**: Integrates data from various OSINT sources
- **Modular Architecture**: Easily extensible with new modules
- **No API Keys Required**: Uses free, public APIs and tools
- **JSON Output**: Structured output for easy parsing and integration
- **Command-Line Interface**: Simple and intuitive CLI usage

## Included Modules

### Core Modules
- **crtsh**: Certificate Transparency logs search
- **maigret**: Username enumeration across social media platforms
- **holehe**: Email address validation and breach checking

### Additional Modules
- **wayback**: Internet Archive Wayback Machine search
- **whois**: Domain registration information lookup
- **dig**: DNS record enumeration
- **ping**: Network connectivity testing
- **shodan**: (Requires API key) IoT device search

## Installation

### Prerequisites
- Python 3.8+
- Required Python packages (see requirements.txt)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### System Dependencies
```bash
# For whois module
sudo apt-get install whois

# For dig module
sudo apt-get install dnsutils

# For ping module
# Usually pre-installed

# For maigret and holehe
pip install maigret holehe
```

## Usage

### Basic Usage
```bash
python aaot.py target@example.com
```

### Advanced Usage
```bash
# Run specific modules
python aaot.py target@example.com -m crtsh,maigret

# Save output to file
python aaot.py target@example.com -o my_scan

# Verbose output
python aaot.py target@example.com -v

# Different output formats
python aaot.py target@example.com -f json
```

### Command Line Options
- `target`: Target domain, IP, or email
- `-m, --modules`: Comma-separated list of modules
- `-o, --output`: Output filename
- `-f, --format`: Output format (json, txt, html)
- `-v, --verbose`: Enable verbose output
- `-c, --config`: Path to config directory

## Configuration

### API Keys
For modules requiring API keys, create `config/api_keys.json`:
```json
{
  "shodan": "your_shodan_api_key"
}
```

### Settings
Modify `config/settings.json` for tool configuration.

## Module Development

### Creating New Modules
1. Inherit from `BaseModule` class
2. Implement `run(target)` method
3. Return standardized response format

Example:
```python
from modules.base_module import BaseModule

class MyModule(BaseModule):
    def run(self, target):
        # Your implementation
        return {
            'target': target,
            'result_count': count,
            'results': data
        }
```

## Output Format

All modules return data in the following JSON format:
```json
{
  "module_name": {
    "target": "target_value",
    "result_count": 5,
    "results": [...]
  }
}
```

## Debugging

### Common Issues

1. **Module Import Errors**
   - Ensure all dependencies are installed
   - Check Python path and module locations

2. **API Rate Limiting**
   - Some modules may have rate limits
   - Implement delays between requests if needed

3. **Network Connectivity**
   - Verify internet connection
   - Check firewall settings

### Debug Mode
Enable verbose output for detailed logging:
```bash
python aaot.py target -v
```

### Manual Module Testing
Test individual modules:
```python
from modules.crtsh_module import CrtshModule
from utils.config_loader import ConfigLoader

config = ConfigLoader()
config.load()
module = CrtshModule(config)
result = module.run("example.com")
print(result)
```

## Stability and Compliance

### Stability Features
- Error handling for all modules
- Timeout protection for long-running operations
- Graceful degradation when modules fail

### Licensing
This project is licensed under Apache License 2.0. See LICENSE file for details.

### Open Source Compliance
- All code is open source
- No proprietary dependencies
- Free for commercial and non-commercial use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Credits

- **Developer**: sigmatsotuff33
- **Email**: sigmatsotuff33@gmail.com
- **GitHub**: https://github.com/sigmatsotuff33-beep
- **Copyright**: 2025 sigmatsotuff33
- **License**: MIT License
## Disclaimer

This tool is for educational and research purposes only. Users are responsible for complying with applicable laws and regulations when using this tool.
Im not involved in any irresponsible uses

## Changelog
I Will Add changelogs inbase of comments and users reply,i only accept *BRUTAL* comments and feedbacks so for making it actually and to actually know whats working and not,thanks.
### Version 1.0.0
- Initial release
- Core modules: crtsh, maigret, holehe
- Additional modules: wayback, whois, dig, ping
- JSON output support
- CLI interface

## POSSIBLE NEW FEATURES:
-A GUI WITH UI 
-TERMINAL GUI
-EASIER COMMANDS
-POSSIBLY EASTER EGGS