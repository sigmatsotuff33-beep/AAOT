import subprocess
import json
from modules.base_module import BaseModule

class HoleheModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)

    def run(self, target):
        try:
            cmd = ["holehe", target, "--json"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return self.parse_response(data, target)
            else:
                return {"error": f"Holehe failed: {result.stderr}", "target": target}

        except subprocess.TimeoutExpired:
            return {"error": "Holehe timeout", "target": target}
        except (subprocess.CalledProcessError, OSError) as e:
            return {"error": str(e), "target": target}

    def parse_response(self, data, target):
        results = []
        for site, info in data.items():
            if info.get('exists'):
                results.append({
                    'site': site,
                    'url': info.get('url', ''),
                    'email': info.get('emailrecovery', ''),
                    'exists': True
                })

        return {
            'target': target,
            'result_count': len(results),
            'results': results
        }
