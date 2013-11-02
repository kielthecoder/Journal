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


