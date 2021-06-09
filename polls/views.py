from django.shortcuts import render
from django.http import HttpResponse


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
def home(request):
	context = {
		'results' :results
	}
	return render(request, 'polls/home.html', context)