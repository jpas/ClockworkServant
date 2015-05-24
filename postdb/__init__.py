_db = {}

with open('./db.txt', 'r') as db:
	for post_id in db:
		_db[post_id[:-1]] = True

def has(id):
	return id in _db

def add(id):
	if not has(id):
		_db[id] = True
		with open('./db.txt', 'a') as db:
			db.write(id + '\n')
