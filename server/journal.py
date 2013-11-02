import cherrypy
import datetime
import markdown
import sqlite3
import jinja2

from models import Post
from views import PostsView

def connect(thread_id):
	# Store a connection to our database in each thread
	cherrypy.thread_data.db = sqlite3.connect('db/test.db')

# Tell CherryPy to call connect for each thread
cherrypy.engine.subscribe('start_thread', connect)

def filter_markdown(text):
	return markdown.markdown(text)

def filter_monthname(month):
	names = [
		"January",
		"February",
		"March",
		"April",
		"May",
		"June",
		"July",
		"August",
		"September",
		"October",
		"November",
		"December"
	]

	return names[month]

class Journal:
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('html'))
	env.filters['markdown'] = filter_markdown
	env.filters['monthname'] = filter_monthname

	def __init__(self):
		self.posts = PostsView(self)

	def _get_cursor(self):
		return cherrypy.thread_data.db.cursor()

	def _get_posts(self, *args):
		cur = self._get_cursor()
		cur.execute(*args)
		posts = []
		for p in cur.fetchall():
			posts.append(Post(p, self))
		cur.close()
		return posts

	@cherrypy.expose
	def index(self):
		posts = self._get_posts('SELECT * FROM posts ORDER BY posted DESC LIMIT 5')
		t = self.env.get_template('index.html')
		return t.render(title="Recent Posts",posts=posts)

	@cherrypy.expose
	def post(self, slug_text):
		cur = self._get_cursor()
		cur.execute('SELECT * FROM posts WHERE slug = ? LIMIT 1', (slug_text,))
		p = Post(cur.fetchone(), self)
		cur.close()
		t = self.env.get_template('view_post.html')
		return t.render(post=p)

if __name__ == '__main__':
	cherrypy.quickstart(Journal())
