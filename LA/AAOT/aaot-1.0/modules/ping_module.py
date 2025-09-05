import subprocess
import json
from modules.base_module import BaseModule

class PingModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)

    def run(self, target):
        try:
            cmd = ["ping", "-c", "4", target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return self.parse_response(result.stdout, target)
            else:
                return {"error": f"Ping failed: {result.stderr}", "target": target}

        except subprocess.TimeoutExpired:
            return {"error": "Ping timeout", "target": target}
        except (subprocess.CalledProcessError, OSError) as e:
            return {"error": str(e), "target": target}

    def parse_response(self, data, target):
        lines = data.strip().split('\n')
        results = []
        for line in lines:
            if 'bytes from' in line or 'icmp_seq' in line:
                results.append(line)

        return {
            'target': target,
            'result_count': len(results),
            'results': results
        }
