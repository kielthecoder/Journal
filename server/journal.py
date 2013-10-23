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

class Post:
	def __init__(self, record=[], parent=None):
		self._id = record[0]
		self.title = record[1]
		self.author_id = record[2]
		self.posted = datetime.datetime.strptime(record[3], "%Y-%m-%d %H:%M:%S")
		self.body = record[4]
		self.slug = record[5]
		self.tags = []
		if parent:
			cur = parent._get_cursor()
			cur.execute('SELECT name FROM tags JOIN tags_to_posts ON tags_to_posts.tag_id = tags.id WHERE tags_to_posts.post_id = %d ORDER BY tags.name ASC' % self._id)
			for tag in cur.fetchall():
				self.tags.append(tag[0])
			cur.close()
		if len(self.tags) == 0:
			self.tags.append("uncategorized")

class Journal:
	env = jinja2.Environment(loader=jinja2.FileSystemLoader('html'))
	env.filters['markdown'] = filter_markdown
	env.filters['monthname'] = filter_monthname

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

	@cherrypy.expose
	def posts(self, *args):
		if len(args) < 1:
			return self._calendar()

		if len(args) > 1:
			if args[1] == 'week':
				return self._posts_from_year_and_week(*args)

			if len(args) == 2:
				return self._posts_from_year_and_month(*args)

		year = args[0]

		return self._posts_from_year(*args)

	def _calendar(self):
		posts = self._get_posts('SELECT * FROM posts ORDER BY posted')
		cal = []

		for p in posts:
			y = p.posted.year
			m = p.posted.month

			matched = False

			for year in cal:
				if year['year'] == y:
					found_month = False

					for month in year['months']:
						if month['month'] == m:
							found_month = True
							month['posts'].append(p)
							matched = True

					if not found_month:
						month = [ { 'month': m, 'posts': [p] } ]
						year['months'].append(month)
						matched = True

				if matched:
					break

			if not matched:
				month = { 'month': m, 'posts': [ p ] }
				year = { 'year': y, 'months': [ month ] }
				cal.append(year)

		t = self.env.get_template('calendar.html')
		return t.render(cal=cal)

	def _posts_from_year(self, *args):
		year = args[0]

		# Get posts within year
		posts = self._get_posts('SELECT * FROM posts WHERE STRFTIME("%Y",posted) = ? ORDER BY posted', (year,))

		t = self.env.get_template('index.html')

		if len(posts) == 1:
			count = "1 post"
		else:
			count = "%d posts" % (len(posts),)

		return t.render(title="%s in %s" % (count, year), posts=posts)

	def _posts_from_year_and_week(self, *args):
		year = args[0]
		week = args[2]

		# Get posts within year and same week
		posts = self._get_posts('SELECT * FROM posts WHERE STRFTIME("%Y",posted) = ? AND STRFTIME("%W",posted) = ? ORDER BY posted', (year, week))

		t = self.env.get_template('index.html')

		if len(posts) == 1:
			count = "1 post"
		else:
			count = "%d posts" % len(posts)

		if len(posts) > 0:
			d1 = posts[0].posted
			d2 = posts[-1].posted
			title = "%s between %s and %s" % (count, d1.strftime("%x"), d2.strftime("%x"))
		else:
			title = count

		return t.render(title=title, posts=posts)

	def _posts_from_year_and_month(self, *args):
		year = args[0]
		month = args[1]

		# Get posts within year and same month
		posts = self._get_posts('SELECT * FROM posts WHERE STRFTIME("%Y",posted) = ? AND STRFTIME("%m",posted) = ? ORDER BY posted', (year, month))

		t = self.env.get_template('index.html')

		if len(posts) == 1:
			count = "1 post"
		else:
			count = "%d posts" % len(posts)

		if len(posts) > 0:
			dt = posts[0].posted
			title = "%s in %s" % (count, dt.strftime("%B %Y"))
		else:
			title = count

		return t.render(title=title, posts=posts)

if __name__ == '__main__':
	cherrypy.quickstart(Journal())
