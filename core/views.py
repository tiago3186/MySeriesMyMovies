from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from core.models import Movie
from django.conf import settings

API_KEY = settings.API_KEY

@login_required
def homepage(request):
    selected_movies = Movie.objects.filter(user=request.user)

    context = {'selected_movies': selected_movies}
    return render(request, 'main.html', context)

@login_required
def search_movie(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        print(search_query)

        # Realize a chamada à API do The Movie DB com o termo de busca
        response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={search_query}')
        data = response.json()

        print(data)

        # Extraia os resultados da busca da resposta JSON
        if 'results' in data:
            results = data['results']
        else:
            results = []

        context = {'results': results, 'search_query': search_query}
        return render(request, 'main.html', context)

    if request.method == 'GET' and 'selected_movies' in request.GET:
        selected_movie_ids = request.GET.getlist('selected_movies')
        selected_movies = []
        for movie_id in selected_movie_ids:
            # Realize uma chamada à API do The Movie DB para obter os detalhes do filme
            response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}')
            movie_data = response.json()

            movie = {
                'title': movie_data['title'],
                'release_date': movie_data['release_date'],
                'average_rating': movie_data['vote_average'],
                'user_rating': 0,  # Você precisará substituir pelo valor real da nota do usuário para o filme
            }
            selected_movies.append(movie)

        context = {'selected_movies': selected_movies}
        
        # Salvar os filmes na biblioteca antes de redirecionar
        for movie in selected_movies:
                Movie.objects.create(
                    title=movie['title'],
                    release_date=movie['release_date'],
                    average_rating=movie['average_rating'],
                    user_rating=movie['user_rating'],
                    user=request.user
                )

        return redirect('main')

    return render(request, 'main.html')

@login_required
def update_user_ratings(request):
    if request.method == 'POST':
        movie_ids = request.POST.getlist('movie_id')
        user_ratings = request.POST.getlist('user_rating')

        for movie_id, user_rating in zip(movie_ids, user_ratings):
            movie = Movie.objects.get(id=movie_id)
            movie.user_rating = user_rating
            movie.save()

    return redirect('main')