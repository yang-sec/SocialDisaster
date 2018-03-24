from json import JSONEncoder

class Tweet(JSONEncoder):
	
	def __init__(self):
		pass
	
	def default(self, o):
		return o.__dict__