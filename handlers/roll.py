import re
from random import randint

def _is_valid_spec(spec):
	return re.match('(\d*?[dD]\d+?)([+-]((\d*?[dD]\d+?)|(\d+?)))*?$', spec)

def _parse(spec):
	if not _is_valid_spec(spec):
		return None

	spec = re.sub('-', '+-', spec);
	dice = re.split('\+', spec)

	for i, v in enumerate(dice):
		if re.match('[1-9]\d?[dD]\d', v):
			count, size = re.split('[dD]', v)
			dice[i] = {
				'count': int(count),
				'size': int(size)
			}
		elif re.match('-?\d+', v):
			dice[i] = int(v)
		else:
			dice[i] = 0

	return dice

def _roll(count, size):
	if count <= 0:
		return 0

	if count == 1:
		return randint(1, size)

	total = 0;
	for die in range(1, count):
		total = total + randint(1, size)

	return total

def _eval(spec):
	parsed = _parse(spec)

	if parsed == None:
		return None

	rolled = 0
	modifier = 0
	for v in parsed:
		if type(v) == int:
			modifier = modifier + v
		else:
			rolled = rolled + _roll(v['count'], v['size'])

	return {
		'total': rolled + modifier,
		'rolled': rolled,
		'modifier': modifier
	}

def is_request(request):
	return request.lower().startswith('roll ')

def handle(spec):
	if is_request(spec):
		spec = spec[5:]

	result = _eval(spec)

	if result == None:
		return None

	if result['modifier'] == 0:
		return 'I rolled **{}** and got **{}**!'.format(spec, result['total'])

	return ('I rolled **{}** and got '
			'**{}**^(_{}_{:+})!').format(spec, result['total'], result['rolled'], result['modifier'])

if __name__ == '__main__':
	import sys
	print handle(' '.join(sys.argv[1:]))
