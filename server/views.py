import cherrypy

class PostsView:
	def __init__(self, parent):
		self.parent = parent
		self.base = parent.base

	def _calendar(self):
		posts = self.parent._get_posts('SELECT * FROM posts ORDER BY posted')
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

		t = self.parent.env.get_template('calendar.html')
		return t.render(base=self.base, cal=cal)

	def _posts_from_year(self, *args):
		year = args[0]

		# Get posts within year
		posts = self.parent._get_posts('SELECT * FROM posts WHERE STRFTIME("%Y",posted) = ? ORDER BY posted', (year,))

		t = self.parent.env.get_template('index.html')

		if len(posts) == 1:
			count = "1 post"
		else:
			count = "%d posts" % (len(posts),)

		return t.render(base=self.base, title="%s in %s" % (count, year), posts=posts)

	def _posts_from_year_and_week(self, *args):
		year = args[0]
		week = args[2]

		# Get posts within year and same week
		posts = self.parent._get_posts('SELECT * FROM posts WHERE STRFTIME("%Y",posted) = ? AND STRFTIME("%W",posted) = ? ORDER BY posted', (year, week))

		t = self.parent.env.get_template('index.html')

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

		return t.render(base=self.base, title=title, posts=posts)

	def _posts_from_year_and_month(self, *args):
		year = args[0]
		month = args[1]

		# Get posts within year and same month
		posts = self.parent._get_posts('SELECT * FROM posts WHERE STRFTIME("%Y",posted) = ? AND STRFTIME("%m",posted) = ? ORDER BY posted', (year, month))

		t = self.parent.env.get_template('index.html')

		if len(posts) == 1:
			count = "1 post"
		else:
			count = "%d posts" % len(posts)

		if len(posts) > 0:
			dt = posts[0].posted
			title = "%s in %s" % (count, dt.strftime("%B %Y"))
		else:
			title = count

		return t.render(base=self.base, title=title, posts=posts)

	@cherrypy.expose
	def default(self, *args):
		if len(args) < 1:
			return self._calendar()

		if len(args) > 1:
			if args[1] == 'week':
				return self._posts_from_year_and_week(*args)

			if len(args) == 2:
				return self._posts_from_year_and_month(*args)

		year = args[0]

		return self._posts_from_year(*args)

