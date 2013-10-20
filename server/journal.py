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
		return t.render(posts=posts)

	@cherrypy.expose
	def test(self):
		cur = self._get_cursor()
		cur.execute('SELECT * FROM posts ORDER BY posted DESC')
		result = cur.fetchone()
		cur.close()
		return str(result)

if __name__ == '__main__':
	cherrypy.quickstart(Journal())
