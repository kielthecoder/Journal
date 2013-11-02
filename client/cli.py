import sys

def new_post_from_file(filename):
	mode = 'body'

	title = ""
	author = ""
	tags = list()
	body = ""

	with open(filename, "rt") as fd:
		for line in fd:
			if line[0:4] == '$END':
				mode = 'end'
			elif line[0:6] == '$TITLE':
				mode = 'title'
				line = line[6:]
				title = line.strip()
				print("title = %r" % title)
			elif line[0:5] == '$TAGS':
				mode = 'tags'
				line = line[5:]
				for tag in line.split():
					tags.append(tag)
				print("tags = %r" % tags)
			else:
				mode = 'body'
				body += line

			if mode == 'end':
				break
	print("body = %r" % body)

	print("Created new post from %s" % filename)

if __name__ == '__main__':
	try:
		if sys.argv[1] == 'new':
			if len(sys.argv) < 3:
				print("Usage: %s new <filename>" % sys.argv[0])
			else:
				new_post_from_file(sys.argv[2])
	except:
		print("Too few arguments")
		print("Usage: %s <command> [args]" % sys.argv[0])
		print("Valid commands are:")
		print("\tnew\t- create a new post")
