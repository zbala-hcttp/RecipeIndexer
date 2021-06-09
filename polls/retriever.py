import sys, lucene
from os import path, listdir

from java.nio.file import Paths

from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer, SimpleAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.search import TermQuery, IndexSearcher
from org.apache.lucene.index import Term, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser


class Retriever:
	
	def __init__(self):
		self.BASE_DIR = path.dirname(path.abspath(sys.argv[0]))
		self.INDEX_DIR = self.BASE_DIR + "/polls/index/"

		if not lucene.getVMEnv():
			self.vm = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
			self.vm.attachCurrentThread()

	def retrieve(self):
		ind_dir = self.INDEX_DIR + "SA/"
		self.vm.attachCurrentThread()
		store = SimpleFSDirectory(Paths.get(ind_dir))
		searcher = IndexSearcher(DirectoryReader.open(store))

		# Create a new retrieving analyzer
		analyzer = StandardAnalyzer()
		query = QueryParser("directions", analyzer).parse("mix in onion")
		topDocs = searcher.search(query, 200).scoreDocs
		docs = []
		for topDoc in topDocs:
		    doc = searcher.doc(topDoc.doc)
		    #print(doc.get("link"))
		    docs.append({"link": doc.get("link"),
		    			 "category": doc.get("category"),
		    			 "name": doc.get("name"),
		    			 "ingredients": doc.get("ingredients"),
		    			 "directions": doc.get("directions")})
		return docs