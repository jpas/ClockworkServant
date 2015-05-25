from os import listdir, path
import re

_srd_path = path.dirname(path.abspath(__file__))

class SRD:
	def __init__(self, folder_name):
		self._path = '{}/{}/'.format(_srd_path, folder_name)
		self._db = set()
		for file in listdir(self._path):
			if path.isfile(path.join(self._path, file)):
				self._db.add(str(file[:-3]))

	def __str__(self):
		return str(self.db)

	def get(self, id):
		if id in self._db:
			file_path = path.join(self._path, id + '.md')
			with open(file_path, 'r') as file:
				return file.read()

		return None

_dbs = {
	'feat': SRD('featdb'),
	'spell': SRD('spelldb')
}

def is_request(request):
	for db in _dbs:
		if request.lower().startswith('srd {} '.format(db)):
			return True

	return False

def handle(spec):
	if is_request(spec):
		spec = spec[4:].lower()
	else:
		return None

	for db_name, db in _dbs.iteritems():
		if spec.startswith(db_name):
			id = re.sub(' ', '-', spec[len(db_name)+1:])
			return db.get(id)


if __name__ == '__main__':
	import sys
	print handle(' '.join(sys.argv[1:]))
