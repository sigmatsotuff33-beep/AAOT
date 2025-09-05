import json
import html
from datetime import datetime
from colorama import Fore

class OutputHandler:

    def __init__(self):
        # No initialization required for OutputHandler
        pass

    def info(self, message):
        print(f"{Fore.CYAN}[*] {message}")

    def warning(self, message):
        print(f"{Fore.YELLOW}[!] {message}")

    def error(self, message):
        print(f"{Fore.RED}[!] {message}")

    def save_results(self, results, filename, format_type="json"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename}_{timestamp}"

        if format_type == "json":
            filename += ".json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)

        elif format_type == "txt":
            filename += ".txt"
            with open(filename, 'w') as f:
                for module, data in results.items():
                    f.write(f"=== {module.upper()} RESULTS ===\n")
                    f.write(f"{json.dumps(data, indent=2)}\n\n")

        elif format_type == "html":
            filename += ".html"
            self._generate_html_report(results, filename)

        return filename

    def _generate_html_report(self, results, filename):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AAOT Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .module { margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
                .module-header { background-color: #f5f5f5; padding: 10px; margin: -15px -15px 15px -15px; border-bottom: 1px solid #ddd; }
                pre { background-color: #f8f8f8; padding: 10px; border-radius: 3px; overflow: auto; }
            </style>
        </head>
        <body>
            <h1>AAOT Report</h1>
            <p>Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        """

        for module, data in results.items():
            html_content += f"""
            <div class="module">
                <div class="module-header">
                    <h2>{module.upper()} Results</h2>
                </div>
                <pre>{html.escape(json.dumps(data, indent=2))}</pre>
            </div>
            """

        html_content += """
        </body>
        </html>
        """

        with open(filename, 'w') as f:
            f.write(html_content)
