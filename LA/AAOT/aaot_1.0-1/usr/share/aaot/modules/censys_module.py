import base64
from modules.base_module import BaseModule

class CensysModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)
        self.api_id = config.api_keys['censys']['api_id']
        self.api_secret = config.api_keys['censys']['api_secret']
        self.base_url = "https://search.censys.io/api/v1/search/certificates"

    def run(self, target):
        auth_str = f"{self.api_id}:{self.api_secret}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        headers = {"Authorization": f"Basic {encoded_auth}"}

        data = {
            'query': target,
            'fields': [
                'parsed.subject.common_name',
                'parsed.names',
                'parsed.validity.start',
                'parsed.validity.end'
            ]
        }

        response = self.make_request(
            self.base_url,
            method="POST",
            data=data,
            headers=headers
        )

        return self.parse_response(response, target)

    def parse_response(self, data, target):
        if 'results' not in data:
            return {"error": "No results found", "target": target}

        results = []
        for cert in data['results'][:10]:
            common_name = cert.get('parsed', {}).get('subject', {}).get('common_name', ['N/A'])[0]
            names = cert.get('parsed', {}).get('names', [])[:5]
            start = cert.get('parsed', {}).get('validity', {}).get('start', 'N/A')
            end = cert.get('parsed', {}).get('validity', {}).get('end', 'N/A')

            results.append({
                'common_name': common_name,
                'names': names,
                'validity': {
                    'start': start,
                    'end': end
                }
            })

        return {
            'target': target,
            'result_count': len(data['results']),
            'results': results
        }
