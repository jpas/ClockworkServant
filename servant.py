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
subreddits = '+'.join(['herasplayground','ClockworkServant'])
hide_string = '######&#009;\n####&#009;\n#####&#009;\n\n'
signature = ('^(We do not guarentee all content in the post is correct.'
			 'If there is a problem with this post, '
			 '[send us a message]'
			 '(http://www.reddit.com/message/compose?to=/r/{0}&subject=Issue%20with%20/u/{0}) '
			 'and we\'ll try to sort it out.)').format(name)
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
		response = ''
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
				if len(signature) + len(final) + len(response) <= 10000:
					response = response + final
		if response == '':
			return None
		return hide_string + response + signature
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
