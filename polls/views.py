from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import retriever

"""
results = [
	{
		"category": "breakfast",
		"name": "egg",
		"ingredients": "1 egg, half cup of milk",
		"directions": "bake egg, add milk"
	},
	{
		"category": "soup",
		"name": "tomato soup",
		"ingredients": "1 tomato, water",
		"directions": "slice tomato, add water"
	}
]
"""

retriever_ = retriever.Retriever()

def home(request):
	recipes= retriever_.retrieve()
	page = request.GET.get('page', 1)
	paginator_ = Paginator(recipes, 10)
	try:
		results = paginator_.page(page)
	except EPageNotAnInteger:
		results = paginator_.page(1)
	except:
		results = paginator_.page(paginator_.num_pages)
	return render(request, 'polls/home.html', {'results' :results})