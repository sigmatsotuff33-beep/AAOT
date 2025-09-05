import subprocess
import json
from modules.base_module import BaseModule

class DigModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)

    def run(self, target):
        try:
            cmd = ["dig", target, "+short"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return self.parse_response(result.stdout, target)
            else:
                return {"error": f"Dig failed: {result.stderr}", "target": target}

        except subprocess.TimeoutExpired:
            return {"error": "Dig timeout", "target": target}
        except (subprocess.CalledProcessError, OSError) as e:
            return {"error": str(e), "target": target}

    def parse_response(self, data, target):
        records = data.strip().split('\n')
        results = [record for record in records if record]

        return {
            'target': target,
            'result_count': len(results),
            'results': results
        }
