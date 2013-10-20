import sqlite3
import cherrypy
import jinja2
import markdown
import datetime

def connect(thread_id):
	# Store a connection to our database in each thread
	cherrypy.thread_data.db = sqlite3.connect('db/test.db')

# Tell CherryPy to call connect for each thread
cherrypy.engine.subscribe('start_thread', connect)

def filter_markdown(text):
	return markdown.markdown(text)

class Post:
	def __init__(self, record=[]):
		self._id = record[0]
		self.title = record[1]
		self.author_id = record[2]
		self.posted = datetime.datetime.strptime(record[3], "%Y-%m-%d %H:%M:%S")
		self.body = record[4]
		self.slug = record[5]

class Journal:
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('html'))
	env.filters['markdown'] = filter_markdown

	def _get_cursor(self):
		return cherrypy.thread_data.db.cursor()

	@cherrypy.expose
	def index(self):
		cur = self._get_cursor()
		cur.execute('SELECT * FROM posts ORDER BY posted DESC')
		posts = []
		for row in cur.fetchall():
			posts.append(Post(row))
		cur.close()
		t = self.env.get_template('index.html')
		return t.render(title="Recent Posts",posts=posts)

	@cherrypy.expose
	def post(self, slug_text):
		cur = self._get_cursor()
		cur.execute('SELECT * FROM posts WHERE slug = ? LIMIT 1', (slug_text,))
		p = Post(cur.fetchone())
		cur.close()
		t = self.env.get_template('view_post.html')
		return t.render(post=p)

	@cherrypy.expose
	def posts(self, *args):
		if len(args) < 1:
			return "TODO: calendar"

		if len(args) > 1:
			if args[1] == 'week':
				return self._posts_from_year_and_week(*args)

		# Posts within the entire year
		cur = self._get_cursor()
		cur.execute('SELECT * FROM posts WHERE STRFTIME("%Y",posted) = ? ORDER BY posted', (args[0],))
		posts = []
		for row in cur.fetchall():
			posts.append(Post(row))
		cur.close()

		t = self.env.get_template('index.html')

		if len(posts) == 1:
			count = "1 post"
		else:
			count = "%d posts" % (len(posts),)

		return t.render(title="%s in %s" % (count, args[0]),posts=posts)

	def _posts_from_year_and_week(self, *args):
		year = args[0]
		month = args[2]

		# Posts within year and same week
		cur = self._get_cursor()
		cur.execute('SELECT * FROM posts WHERE STRFTIME("%Y",posted) = ? AND STRFTIME("%W",posted) = ? ORDER BY posted', (year, month))
		posts = []
		for row in cur.fetchall():
			posts.append(Post(row))
		cur.close()

		t = self.env.get_template('index.html')
		d1 = posts[0].posted
		d2 = posts[-1].posted

		if len(posts) == 1:
			count = "1 post"
		else:
			count = "%d posts" % (len(posts),)

		return t.render(title="%s between %s and %s" % (count, d1.strftime("%x"), d2.strftime("%x")), posts=posts)

if __name__ == '__main__':
	cherrypy.quickstart(Journal())
