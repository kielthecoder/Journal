import sys

if __name__ == '__main__':
	try:
		if sys.argv[1] == 'new':
			if len(sys.argv) < 3:
				print("Usage: %s new <filename>" % sys.argv[0])
			else:
				pass
	except:
		print("Too few arguments")
		print("Usage: %s <command> [args]" % sys.argv[0])
		print("Valid commands are:")
		print("\tnew\t- create a new post")
