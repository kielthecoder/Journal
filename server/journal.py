import sqlite3
import json

from cherrypy import engine, expose, quickstart, response, thread_data
from markdown import markdown
from jinja2 import Environment, FileSystemLoader
from models import Post
from views import PostsView

# Database callbacks

def connect(thread_id):
	# Store a connection to our database in each thread
	thread_data.db = sqlite3.connect('db/test.db')

engine.subscribe('start_thread', connect)

# Jinja2 filter callbacks

def filter_markdown(text):
	return markdown(text)

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

# Function decorators

def jsonify(func):
	def wrapper(*args, **kwargs):
		res = func(*args, **kwargs)
		response.headers['Content-Type'] = "application/json"
		return bytes(json.dumps(res), encoding='utf-8')
	return wrapper

# Client API

class APIv1:
	def __init__(self, parent):
		self.parent = parent

	def _new_post(self, *args, **kwargs):
		html = "<html><body>"
		html += "<title>" + kwargs['title'] + "</title>"
		html += "<tags>" + kwargs['tags'] + "</tags>"
		html += "<body>" + kwargs['body'] + "</body>"
		html += "</body></html>"
		return html

	@expose
	@jsonify
	def default(self, *args, **kwargs):
		return { 'status': 'TODO' }

class API:
	def __init__(self, parent):
		self.v1 = APIv1(parent)

# Server

class Journal:
	env = Environment(loader=FileSystemLoader('html'))
	env.filters['markdown'] = filter_markdown
	env.filters['monthname'] = filter_monthname

	def __init__(self, base):
		self.base = base
		self.posts = PostsView(self)
		self.api = API(self)

	def _get_cursor(self):
		return thread_data.db.cursor()

	def _get_posts(self, *args):
		cur = self._get_cursor()
		cur.execute(*args)
		posts = []
		for p in cur.fetchall():
			posts.append(Post(p, self))
		cur.close()
		return posts

	@expose
	def index(self):
		posts = self._get_posts('SELECT * FROM posts ORDER BY posted DESC LIMIT 5')
		t = self.env.get_template('index.html')
		return t.render(title="Recent Posts", base=self.base, posts=posts)

	@expose
	def post(self, slug_text):
		cur = self._get_cursor()
		cur.execute('SELECT * FROM posts WHERE slug = ? LIMIT 1', (slug_text,))
		p = Post(cur.fetchone(), self)
		cur.close()
		t = self.env.get_template('view_post.html')
		return t.render(base=self.base, post=p)

if __name__ == '__main__':
	quickstart(Journal('/app1'), config={
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': '/home/kiel/journal/html/static',
		}
	})
