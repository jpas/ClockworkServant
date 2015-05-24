from os.path import abspath, dirname

_db_path = dirname(abspath(__file__)) + '/db.txt'
_db = {}

with open(_db_path, 'r') as db:
	for post_id in db:
		_db[post_id[:-1]] = True

def has(id):
	return id in _db

def add(id):
	if not has(id):
		_db[id] = True
		with open(_db_path, 'a') as db:
			db.write(id + '\n')
