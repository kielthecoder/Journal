import cherrypy

class TwoView:
	@cherrypy.expose
	def index(self, year=None, month=None, day=None):
		html = "From the TWO class, received: "
		if year:
			html += "year = %s " % year
		if month:
			html += "month = %s " % month
		if day:
			html += "day = %s " % day
		return html

	@cherrypy.expose
	def default(self, *args):
		html = "No match, but got this: "
		for arg in args:
			html += arg + " "
		return html

class OneView:
	def __init__(self):
		self.two = TwoView()

	@cherrypy.expose
	def index(self):
		return "This will be the view of the ONE class"

class TestingApp:
	one = OneView()

	@cherrypy.expose
	def index(self):
		return "Hello!"

if __name__ == '__main__':
	cherrypy.quickstart(TestingApp())

