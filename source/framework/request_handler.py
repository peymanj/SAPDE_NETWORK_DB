import requests
import datetime
import json

def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            pass
    return json_dict

# loaded_dict = json.loads(dumped_dict, object_hook=date_hook)

class RequestHandler:

	@staticmethod
	def get(url, params):
		r = requests.get(url=url, params=params)
		res = json.loads(r.text, object_hook=date_hook)
		# res = r.json()
		# res['request'] = r
		return res
	@staticmethod
	def post(url, params):
		r = requests.post(url=url, data=params)
		res = json.loads(r.text, object_hook=date_hook)

		# res = r.json()
		# res['request'] = r
		return res
