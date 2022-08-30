from django.views import generic

from .models import Movie

class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 100
    # context -> object_list
    queryset = Movie.objects.all().order_by('-rating_avg')


movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    # context -> object -> id
    queryset = Movie.objects.all()


movie_detail_view = MovieDetailView.as_view()