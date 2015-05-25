from os.path import abspath, dirname

_db_path = dirname(abspath(__file__)) + '/db.txt'
_db = set()

with open(_db_path, 'r') as db:
	for post_id in db:
		_db.add(post_id)

def has(id):
	return id in _db

def add(id):
	if id not in _db:
		_db.add(id)
		with open(_db_path, 'a') as db:
			db.write(id + '\n')
