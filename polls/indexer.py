import sys, lucene
from os import path, listdir

from java.nio.file import Paths

from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer, SimpleAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions

class Indexer:
	
	def __init__(self, _BASE_DIR):
		self.INPUT_DIR = _BASE_DIR + "/input/"
		self.INDEX_DIR = _BASE_DIR + "/index/"
		self.NoT = 1000000
		#self.initializeVM()

	def initializeVM(self):
		if not lucene.getVMEnv():
			lucene.initVM(vmargs=['-Djava.awt.headless=true'])

	def createIndexer(self, _analyzer):
		if _analyzer == 'English Analyzer':
			ind_dir = self.INDEX_DIR + "EA/"
			analyzer =  EnglishAnalyzer()
		elif _analyzer == 'Standard Analyzer':
			ind_dir = self.INDEX_DIR + "SA/"
			analyzer =  StandardAnalyzer()
		elif _analyzer == 'Whitespace Analyzer':
			ind_dir = self.INDEX_DIR + "WA/"
			analyzer =  WhitespaceAnalyzer()
		else:
			ind_dir = self.INDEX_DIR + "SIMPA/"
			analyzer =  SimpleAnalyzer()

		# Create a new directory. As a SimpleFSDirectory
		store= SimpleFSDirectory(Paths.get(ind_dir))
		analyzer = LimitTokenCountAnalyzer(analyzer, self.NoT)
		config = IndexWriterConfig(analyzer)
		config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
		writer = IndexWriter(store, config)

		with open(self.INPUT_DIR+"/recipes.txt","r") as input_file:
			recipes = input_file.readlines()
			input_file.close()

		fieldTypeLink = FieldType()
		fieldTypeLink.setIndexOptions( IndexOptions.DOCS )
		fieldTypeLink.setStored( True )
		fieldTypeLink.setTokenized( False )
		fieldTypeLink.freeze()

		fieldTypeText = FieldType()
		fieldTypeText.setIndexOptions( IndexOptions.DOCS_AND_FREQS_AND_POSITIONS )
		fieldTypeText.setTokenized( True )
		fieldTypeText.setStored( True )
		fieldTypeText.freeze()

		recipes = [x.strip() for x in recipes]
		for recipe in recipes:
			elements = recipe.split("|")
			doc = Document()
			doc.add(Field("link", elements[0], fieldTypeLink))
			doc.add(Field("category", elements[1], fieldTypeText))
			doc.add(Field("name", elements[2], fieldTypeText))
			doc.add(Field("ingredients", elements[3], fieldTypeText))
			doc.add(Field("directions", elements[4], fieldTypeText))
			writer.addDocument(doc)

		writer.commit()
		writer.close()



BASE_DIR = path.dirname(path.abspath(sys.argv[0]))

indexer_ = Indexer(BASE_DIR)

indexer_.createIndexer("English Analyzer")
indexer_.createIndexer("Standard Analyzer")
indexer_.createIndexer("Whitespace Analyzer")
indexer_.createIndexer("Simple Analyzer")	
