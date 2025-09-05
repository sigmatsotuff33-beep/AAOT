import requests
from modules.base_module import BaseModule

class WaybackModule(BaseModule):

    def __init__(self, config):
        super().__init__(config)
        self.base_url = "http://web.archive.org/cdx/search/cdx"

    def run(self, target):
        params = {
            "url": target,
            "output": "json",
            "limit": 10,
            "filter": "statuscode:200"
        }
        try:
            response = self.make_request(self.base_url, params=params)
            return self.parse_response(response, target)
        except RuntimeError as e:
            return {"error": str(e), "target": target}

    def parse_response(self, data, target):
        if not data or len(data) < 2:
            return {
                'target': target,
                'result_count': 0,
                'results': []
            }
        results = []
        # Skip the first entry as it is the header
        for entry in data[1:11]:
            results.append({
                'timestamp': entry[1],
                'original': entry[2],
                'mimetype': entry[3],
                'statuscode': entry[4],
                'digest': entry[5],
                'length': entry[6]
            })
        return {
            'target': target,
            'result_count': len(results),
            'results': results
        }
