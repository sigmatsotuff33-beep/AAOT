import subprocess
import json
from modules.base_module import BaseModule

class MaigretModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)

    def run(self, target):
        try:
            cmd = ["maigret", target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return self.parse_response(data, target)
            else:
                return {"error": f"Maigret failed: {result.stderr}", "target": target}

        except subprocess.TimeoutExpired:
            return {"error": "Maigret timeout", "target": target}
        except (subprocess.CalledProcessError, OSError) as e:
            return {"error": str(e), "target": target}

    def parse_response(self, data, target):
        results = []
        for site, info in data.items():
            if info.get('status') == 'found':
                results.append({
                    'site': site,
                    'url': info.get('url', ''),
                    'username': info.get('username', ''),
                    'status': 'found'
                })

        return {
            'target': target,
            'result_count': len(results),
            'results': results
        }
