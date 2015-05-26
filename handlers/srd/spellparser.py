from bs4 import BeautifulSoup
from html2text import HTML2Text
import re
import urllib
import os
from inflector import Inflector

titleize = Inflector().titleize

to_markdown = HTML2Text()
to_markdown.body_width = 0
to_markdown = to_markdown.handle

def to_ascii(string):
	string = unicode(string)
	new_string = ''
	for char in string:
		if ord(char) < 128:
			new_string = new_string + char
	return new_string

def parse(html):
	spells = []
	index = -1
	for descendant in BeautifulSoup(html, 'html5lib').find(id='ctl00_MainContent_DataListTypes_ctl00_LabelName').descendants:
		descendant = to_ascii(descendant)
		if descendant.startswith('<h1'):
			spells.append('')
			index = index + 1
		if index >= 0:
			spells[index] = spells[index] + descendant

	for i, spell in enumerate(spells):
		soup = BeautifulSoup(spell, 'html5lib').body

		spell = {}

		spell['name'] = soup.h1.get_text().strip()
		spell['url']  = urllib.quote(spell['name'])
		spell['id']   = re.sub('[^\w]', '-', spell['name'].lower())
		spell['id']   = re.sub('([\w-]+?)--(\w+)', '\\2-\\1', spell['id'])

		spell['pfs'] = hasattr(soup.h1, 'img')

		spell['source'] = {
			'link': soup.a['href'][:34],
			'book': soup.a.get_text().split(' pg. ')[0],
			'page': soup.a.get_text().split(' pg. ')[1]
		}

		if spell['source']['page'] == '1':
			spell['source']['page'] = '**LOOKUP**'

		spell['text'] = to_markdown(to_ascii(soup))
		spell['text'] = re.sub('\*\*([\w ]+)\*\*\\1', '**\\1**', spell['text'])
		spell['text'] = re.sub('_([a-z ]+)_\\1', '_[\\1]_', spell['text'])
		spell['text'] = re.sub('_([\w ]+)_\\1', '_\\1_', spell['text'])
		spell['text'] = re.sub('([\w ]+)\n\n\\1', '\\1\n\n', spell['text'])
		spell['text'] = re.sub(' \]_', ']_ ', spell['text'])
		spell['text'] = re.sub('.*\*\*Source\*\*.*\n', '', spell['text'])
		spell['text'] = re.sub('.*Amazon.*', '', spell['text'])
		spell['text'] = re.sub('.*\*\*\*\*.*', '', spell['text'])
		spell['text'] = '\n\n'.join(spell['text'].strip().split('\n')[1:])
		spell['text'] = re.sub('(?m)\n[\s]+', '\n\n', spell['text']).strip()

		header = '# Spell: {}\n\n'.format(spell['name'])
		header = header + '^([{}][ss-{}] pg. {} | '.format(spell['source']['book'], spell['id'], spell['source']['page'])
		if spell['pfs']:
			header = header + 'PFS Legal | '
		header = header + '[Archives of Nehtys][sn-{}])\n\n'.format(spell['id'])

		spell['text'] = header + spell['text']

		spell['text'] = spell['text'] + '\n\n[ss-{}]: {}\n'.format(spell['id'], spell['source']['link'])
		spell['text'] = spell['text'] + '[sn-{}]: http://www.archivesofnethys.com/SpellDisplay.aspx?ItemName={}'.format(spell['id'], spell['url'])

		related = set(re.findall('_\[[a-z ]+\]_', spell['text']))

		for name in related:
			name = name[2:-2]
			url  = titleize(name.strip())
			url  = re.sub('Lesser (.*)', '\\1, Lesser', url)
			url  = re.sub('Greater (.*)', '\\1, Greater', url)
			url  = re.sub('Communal (.*)', '\\1, Communal', url)
			url  = urllib.quote(name)
			spell['text'] = spell['text'] + '\n[{}]: http://www.archivesofnethys.com/SpellDisplay.aspx?ItemName={}'.format(name, url)

		spell['file'] = spell['id'] + '.md'

		spells[i] = spell
	return spells

def get(spell_name):
	url = 'http://www.archivesofnethys.com/SpellDisplay.aspx?ItemName=' + urllib.quote(spell_name)
	print url
	html = urllib.urlopen(url).read()
	return parse(html)

def write(spell_name, base_path):
	for spell in get(spell_name):
		print spell['file']
		path = os.path.join(base_path, 'spelldb', spell['file'])
		with open(path, 'w') as file:
			file.write(spell['text'])

cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'spells.txt'), 'r') as spells:
	for spell in spells:
		write(spell[:-1], cwd)
