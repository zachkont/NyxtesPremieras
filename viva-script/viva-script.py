from html.parser import HTMLParser
import requests
import json
import datetime
from dateutil.parser import parse

class Movie():
	
	def __init__(self, date=None, time=None, title=None, cinema=None, description=None):
		self.date = date
		self.time = time
		self.title = title
		self.cinema = cinema
		self.description = description

	def displayMovie(self):
		print("Date: ", self.date)
		print("Time: ", self.time)
		print("Title: ", self.title)
		print("Cinema: ", self.cinema)
		print("Description: ", self.description)
		return

	def toObject(self):
		if "Σεπτεμβρίου" in self.date:
			self.date = 'Wed, 18/9'
			self.time = '12:00'
		return {
			"id": 0,
			"date": self.date,
			"time": self.time,
			"director": "director goes here",
			"datetime": datetime.datetime.strptime(self.date + ' ' + self.time, '%a, %d/%m %H:%M').isoformat(),
			# "datetime": datetime.datetime.fromisoformat(parse(self.date + ' ' + self.time)),
			"title": self.title,
			"subtitle": "subtitle goes here",
			"room": self.cinema,
			# "description": self.description,
			"description": "description goes here",
			"isparty": "makeFalse",
        	"isfirst": "makeFalse",
        	"selected": "makeFalse"
		}

class DescriptionParser(HTMLParser):
	description = ""
	writeAttr = False

	def handle_starttag(self, tag, attrs):
		if (tag == "div"):
			for name, values in attrs:
				if self.isDescription(name, values):
					DescriptionParser.writeAttr = True

	def handle_endtag(self, tag):
		if (tag == "div") and (DescriptionParser.writeAttr):
			DescriptionParser.writeAttr = False

	def handle_data(self, data):
		if (DescriptionParser.writeAttr):
			DescriptionParser.description += data + "\n\n"

	def isDescription(self, attributeName, values):
		if (attributeName == "itemprop") and (values == "description"):
			return True
		return False

class Parser(HTMLParser):

	movies = []
	moviesCounter = 0
	writeAttr = False
	tmpAttr = None
	tmpMovie = {
		"date": None,
		"time": None,
		"title": None,
		"cinema": None,
		"description": None
	}

	def handle_starttag(self, tag, attrs):

		if (tag == "div"):
			for name, values in attrs:

				# Movie tag begins
				if self.isMovie(name, values):
					Parser.moviesCounter += 1
					# print(Parser.moviesCounter)
					return

				if self.isDate(name, values):
					Parser.writeAttr = True
					Parser.tmpAttr = "date"

				if self.isTime(name, values):
					Parser.writeAttr = True
					Parser.tmpAttr = "time"

		if (tag == "span"):
			for name, values in attrs:

				if self.isTitle(name, values):
					Parser.writeAttr = True
					Parser.tmpAttr = "title"

				if self.isCinema(name, values):
					Parser.writeAttr = True
					Parser.tmpAttr = "cinema"

		# if (tag == "a"):
		# 	for name, values in attrs:
		# 		if self.isDescription(name, values):
		# 			Parser.writeAttr = True
		# 			Parser.tmpAttr = "description"

		# 	for name, values in attrs:
		# 		if (name == "href") and (Parser.writeAttr) and (Parser.tmpAttr == "description"):
		# 			link = "https://www.viva.gr" + values
		# 			self.saveDescription(link)
		# 			Parser.writeAttr = False

		return


	def handle_endtag(self, tag):
		# print("Encountered an end tag :", tag)
		return

	def handle_data(self, data):

		if (Parser.writeAttr):
			Parser.tmpMovie[Parser.tmpAttr] = data
			Parser.writeAttr = False

		if (Parser.tmpAttr == "cinema"):
			date = Parser.tmpMovie["date"]
			date = date.replace("Πεμ", "Thu")
			date = date.replace("Παρ", "Fri")
			date = date.replace("Σαβ", "Sat")
			date = date.replace("Κυρ", "Sun")
			date = date.replace("Δευ", "Mon")
			date = date.replace("Τρι", "Tue")
			date = date.replace("Τετ", "Wed")
			time = Parser.tmpMovie["time"]
			title = Parser.tmpMovie["title"]
			cinema = Parser.tmpMovie["cinema"]
			description = Parser.tmpMovie["description"]
			Parser.movies.append( Movie( date, time, title, cinema, description ) )

		return

	def saveDescription(self, link):
		res = requests.get(link).text
		dcp = DescriptionParser()
		dcp.feed(res)
		Parser.tmpMovie["description"] = dcp.description
		dcp.description = ""
		return

	def isMovie(self, attributeName, values):
		if (attributeName == "class") and ("events-container__item" in values.split()):
			return True
		return False

	def isDate(self, attributeName, values):
		if (attributeName == "class") and ("events-container__item-date" in values.split()):
			return True
		return False

	def isTime(self, attributeName, values):
		if (attributeName == "class") and ("events-container__item-time" in values.split()):
			return True
		return False

	def isTitle(self, attributeName, values):
		if (attributeName == "class") and ("events-container__item-play" in values.split()):
			return True
		return False

	def isCinema(self, attributeName, values):
		if (attributeName == "class") and ("events-container__item-venue" in values.split()):
			return True
		return False

	def isDescription(self, attributeName, values):
		if (attributeName == "title") and ("Κράτηση" in values.split()):
			return True
		return False


response = requests.get("https://www.viva.gr/tickets/venues/nyxtes-premieras/")
htmlDoc = response.text

parser = Parser()
parser.feed(htmlDoc)
# print(parser.tmpMovie)

movies = []

# print("const movies = [")

for movie in parser.movies:
	movieObject = movie.toObject()
	if movieObject not in movies:
		# movie.displayMovie()
		# print(movie.toObject())
		# print(",")
		movies.append(movieObject)

index = 0
for movie in movies:
	movie["id"] = index
	index = index + 1
	

# print("]")
print(json.dumps(movies, ensure_ascii=False))

# print(len(parser.movies))
# print("SUNOLO TAINIWN: ", parser.moviesCounter)
parser.close()

# classes in divs:
# events-container__item:
# events-container__item-date
# events-container__item-time
# events-container__item-play  || titlos
# events-container__item-venue || cinema
# <a> with class: eb-button eb-button--primary
