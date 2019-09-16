from html.parser import HTMLParser
import requests
import json

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
		return {
			"date": self.date,
			"time": self.time,
			"title": self.title,
			"cinema": self.cinema,
			"description": self.description
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
					print(Parser.moviesCounter)
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
			Parser.movies.append( Movie( Parser.tmpMovie["date"], Parser.tmpMovie["time"], Parser.tmpMovie["title"], Parser.tmpMovie["cinema"], Parser.tmpMovie["description"] ) )

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

movies = {
	"movies": []
}

# print("{"movies": [)")
# for movie in parser.movies:
	# movie.displayMovie()
	# print(movie.toObject())
	# print(",")
	# movies["movies"].append( movie.toObject() )

# print("]}")
# print( json.dumps(movies) )

print(len(parser.movies))
# print("SUNOLO TAINIWN: ", parser.moviesCounter)

parser.close()

# classes in divs:
# events-container__item:
# events-container__item-date
# events-container__item-time
# events-container__item-play  || titlos
# events-container__item-venue || cinema
# <a> with class: eb-button eb-button--primary
