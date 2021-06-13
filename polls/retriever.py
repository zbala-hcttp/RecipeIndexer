import sys, lucene
from os import path, listdir

from java.nio.file import Paths

from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer, SimpleAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.search import TermQuery, IndexSearcher, BooleanClause
from org.apache.lucene.index import Term, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser


class Retriever:
	
	def __init__(self):
		self.BASE_DIR = path.dirname(path.abspath(sys.argv[0]))
		self.INDEX_DIR = self.BASE_DIR + "/polls/index/"

		if not lucene.getVMEnv():
			self.vm = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
			self.vm.attachCurrentThread()

		self.SHOULD = BooleanClause.Occur.SHOULD

	def retrieve(self, fields_, query_, analyzer_):
		self.vm.attachCurrentThread()

		# Create a new retrieving analyzer
		if analyzer_ == "opt1":
			ind_dir = self.INDEX_DIR + "SIMPA/"
			analyzer = SimpleAnalyzer()
		elif analyzer_ == "opt2":
			analyzer = WhitespaceAnalyzer()
			ind_dir = self.INDEX_DIR + "WA/"
		elif analyzer_ == "opt3":
			analyzer = EnglishAnalyzer()
			ind_dir = self.INDEX_DIR + "EA/"
		else:
			analyzer = StandardAnalyzer()
			ind_dir = self.INDEX_DIR + "SA/"

		store = SimpleFSDirectory(Paths.get(ind_dir))
		searcher = IndexSearcher(DirectoryReader.open(store))

		fields = []
		sh = []
		for keys in fields_.keys():
			if fields_[keys]:
				fields.append(keys)
				sh.append(self.SHOULD)

		if query_ == None or query_ == "":
			query_ = "abcdef"

		query = query = MultiFieldQueryParser.parse(query_, fields, sh, analyzer)
		topDocs = searcher.search(query, 50).scoreDocs
		docs = []
		for topDoc in topDocs:
		    doc = searcher.doc(topDoc.doc)
		    docs.append({"link": doc.get("link"),
		    			 "category": doc.get("category"),
		    			 "name": doc.get("name"),
		    			 "ingredients": doc.get("ingredients"),
		    			 "directions": doc.get("directions")})
		return docs