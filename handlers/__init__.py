import pointbuy
import roll

handlers = {
	'pointbuy': pointbuy,
	'roll': roll
}

def has(requests):
	for request in requests:
		for handle in handlers.itervalues():
			if (handle.is_request(request)):
				return True

	return False

def handle(request):
	for handler in handlers.itervalues():
		if handler.is_request(request):
			return handler.handle(request)

	return None

if __name__ == '__main__':
	import sys
	print handle(' '.join(sys.argv[1:]))
