import subprocess
import json
from modules.base_module import BaseModule

class WhoisModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)

    def run(self, target):
        try:
            cmd = ["whois", target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return self.parse_response(result.stdout, target)
            else:
                return {"error": f"Whois failed: {result.stderr}", "target": target}

        except subprocess.TimeoutExpired:
            return {"error": "Whois timeout", "target": target}
        except (subprocess.CalledProcessError, OSError) as e:
            return {"error": str(e), "target": target}

    def parse_response(self, data, target):
        # Simple parsing, extract key fields
        lines = data.split('\n')
        info = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()

        return {
            'target': target,
            'result_count': len(info),
            'results': info
        }
