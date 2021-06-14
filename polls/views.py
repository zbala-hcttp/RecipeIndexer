from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import retriever


fields = {
	"category" : False,
	"name" : False,
	"ingredients" : False,
	"directions" : False
}

retriever_ = retriever.Retriever()

def home(request):
	if "category" in request.GET:
		fields["category"] = True
	else:
		fields["category"] = False
	if "name" in request.GET:
		fields["name"] = True
	else:
		fields["name"] = False
	if "ingredients" in request.GET:
		fields["ingredients"] = True
	else:
		fields["ingredients"] = False
	if "directions" in request.GET:
		fields["directions"] = True
	else:
		fields["directions"] = False

	query = request.GET.get("query")
	analyzer = request.GET.get("analyzer")

	recipes= retriever_.retrieve(fields, query, analyzer)
	page = request.GET.get('page', 1)
	paginator_ = Paginator(recipes, 5)
	try:
		results = paginator_.page(page)
	except EPageNotAnInteger:
		results = paginator_.page(1)
	except:
		results = paginator_.page(paginator_.num_pages)
	return render(request, 'polls/home.html', {'results' : results, 'fields' : fields, 'query' : query, 'analyzer' : analyzer, 'total' : len(recipes)})