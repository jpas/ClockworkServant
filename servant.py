import re
from time import sleep
import praw

import postdb
import handlers

name = 'ClockworkServant'
author = 'Octordia'
# use semantic versioning
version = '0.1.0'
user_agent = '{}:{} (by /u/v{})'.format(name, version, author)
# the subreddits that the bot will watch for selfposts
subreddits = '+'.join(['herasplayground'])
sleep_time = 5

def has_not_posted(id, replies):
	if postdb.has(str(id)):
		return False

	if replies != None:
		for reply in replies:
			postdb.add(str(id))
			return False

	return True

def create_reply(id, body):
	requests = set(re.findall('/u/{} (.*)'.format(name), body))
	if handlers.has(requests):
		print 'Preparing reply for {}'.format(id)
		response = '######&#009;\n####&#009;\n#####&#009;\n\n'
		for request in requests:
			result = handlers.handle(request)
			if result != None:
				final = ''
				for line in result.split('\n'):
					if line != '':
						if not line.startswith('['):
							line = '> ' + line
						final = final + line + '\n\n'
				final = final + '---\n'
				if len(final) + len(response) - 6 <= 10000:
					response = response + final
		return response[:-6]
	return None

reddit = praw.Reddit(user_agent=user_agent, site_name=name)
print 'Autheticating with reddit'
reddit.login()

print 'Starting {} loop'.format(name)
while True:
	for post in list(reddit.get_subreddit(subreddits).get_new()):
		if has_not_posted(post.id, post.comments):
			reply = create_reply(post.id, post.selftext)
			if reply != None:
				post.add_comment(reply)
				postdb.add(post.id)

	for comment in (list(reddit.get_mentions()) + list(reddit.get_unread())):
		if comment.was_comment and has_not_posted(comment.id, comment.replies):
			reply = create_reply(comment.id, comment.body)
			if reply != None:
				comment.reply(reply)
				postdb.add(comment.id)
				comment.mark_as_read()

	print 'sleeping for {} seconds'.format(sleep_time)
	sleep(sleep_time)
