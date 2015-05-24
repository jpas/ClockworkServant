import re

def _is_valid_spec(spec):
	return re.match('\d{1,2}( \d{1,2}){5}', spec)

def _parse(spec):
	if not _is_valid_spec(spec):
		return None

	scores = re.split(' ', spec)

	for i, score in enumerate(scores):
		score = int(score)
		if score > 18 or score < 7:
			return None

	return scores

_points = {
	'7': -4,
	'8': -2,
	'9': -1,
	'10': 0,
	'11': 1,
	'12': 2,
	'13': 3,
	'14': 5,
	'15': 7,
	'16': 10,
	'17': 13,
	'18': 17
}

def _eval(spec):
	scores = _parse(spec)

	if scores == None:
		return None

	total = 0
	for i, score in enumerate(scores):
		total = total + _points[score]
		scores[i] = '{} ({})'.format(score, _points[score])

	return total

def is_request(request):
	return request.lower().startswith('pointbuy ')

def handle(spec):
	if is_request(spec):
		spec = spec[9:]

	result = _eval(spec);

	if result == None:
		return 'I tried to calculate the point buy value of **{}** but I can figure it out!'.format(spec)

	return 'I calculated the point buy value for **{}** for you, it is **{}**!'.format(spec, result)

if __name__ == '__main__':
	import sys
	print handle(' '.join(sys.argv[1:]))
