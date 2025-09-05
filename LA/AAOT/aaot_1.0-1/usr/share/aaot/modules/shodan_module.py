from modules.base_module import BaseModule

class ShodanModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)
        self.api_key = config.api_keys['shodan']
        self.base_url = "https://api.shodan.io"

    def run(self, target):
        params = {
            "key": self.api_key,
            "query": target
        }

        response = self.make_request(
            f"{self.base_url}/shodan/host/search",
            params=params
        )

        return self.parse_response(response, target)

    def parse_response(self, data, target):
        if 'matches' not in data:
            return {"error": "No results found", "target": target}

        results = []
        for host in data['matches'][:5]:
            results.append({
                'ip': host.get('ip_str', 'N/A'),
                'port': host.get('port', 'N/A'),
                'org': host.get('org', 'N/A'),
                'hostnames': host.get('hostnames', [])
            })

        return {
            'target': target,
            'result_count': len(data['matches']),
            'results': results
        }
