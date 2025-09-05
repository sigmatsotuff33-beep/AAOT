from modules.base_module import BaseModule

class CrtshModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)
        self.base_url = "https://crt.sh"

    def run(self, target):
        params = {
            "q": target,
            "output": "json"
        }

        response = self.make_request(
            f"{self.base_url}/",
            params=params
        )

        return self.parse_response(response, target)

    def parse_response(self, data, target):
        if not data:
            return {
                'target': target,
                'result_count': 0,
                'results': []
            }

        results = []
        for entry in data[:10]:
            results.append({
                'issuer_ca_id': entry.get('issuer_ca_id', 'N/A'),
                'issuer_name': entry.get('issuer_name', 'N/A'),
                'common_name': entry.get('common_name', 'N/A'),
                'name_value': entry.get('name_value', 'N/A'),
                'entry_timestamp': entry.get('entry_timestamp', 'N/A')
            })

        return {
            'target': target,
            'result_count': len(data),
            'results': results
        }
