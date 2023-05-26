from django.shortcuts import render

# Create your views here.

from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests

@login_required
def homepage(request):
    return render(request, 'main.html')

@login_required
def search_movie(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        print(search_query)
        api_key = '1e440f65016c5cbd7a4d5712968422a2'  # Substitua por sua chave de API do The Movie DB

        # Realize a chamada à API do The Movie DB com o termo de busca
        response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={search_query}')
        data = response.json()

        print(data)

        # Extraia os resultados da busca da resposta JSON
        if 'results' in data:
            results = data['results']
        else:
            results = []

        context = {'results': results, 'search_query': search_query}
        return render(request, 'main.html', context)

    return render(request, 'main.html')
