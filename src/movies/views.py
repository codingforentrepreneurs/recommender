from django.views import generic

from .models import Movie


SORTING_CHOICES = {
    "popular": "popular",
    "unpopular": "unpopular",
    "top rated": "-rating_avg",
    "low rated": "rating_avg",
    "recent": "-release_date",
    "old": "release_date"
}


class MovieListView(generic.ListView):
    paginate_by = 100
    # context -> object_list

    def get_queryset(self):
        request = self.request
        sort = request.GET.get('sort') or request.session.get('movie_sort_order') or 'popular'
        qs =  Movie.objects.all()
        if sort is not None:
            request.session['movie_sort_order'] = sort
            if sort == 'popular':
                return qs.popular()
            elif sort == 'unpopular':
                return qs.popular(reverse=True)
            qs = qs.order_by(sort)
        return qs

    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ['movies/snippet/list.html']
        return ['movies/list-view.html']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        context['sorting_choices'] = SORTING_CHOICES
        if user.is_authenticated:
            object_list = context['object_list']
            object_ids = [x.id for x in object_list]
            my_ratings =  user.rating_set.movies().as_object_dict(object_ids=object_ids)
            context['my_ratings'] = my_ratings
        return context


movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    # context -> object -> id
    queryset = Movie.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            object = context['object']
            object_ids = [object.id]
            my_ratings =  user.rating_set.movies().as_object_dict(object_ids=object_ids)
            context['my_ratings'] = my_ratings
        return context


movie_detail_view = MovieDetailView.as_view()


class MovieInfiniteRatingView(MovieDetailView):
    def get_object(self):
        user = self.request.user
        # exclude_ids = []
        # if user.is_authenticated:
        #     exclude_ids = [x.object_id for x in user.rating_set.filter(active=True)]
        return Movie.objects.all().order_by("?").first()
    
    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ['movies/snippet/infinite.html']
        return ['movies/infinite-view.html']


movie_infinite_rating_view = MovieInfiniteRatingView.as_view()




class MoviePopularView(MovieDetailView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['endless_path'] = '/movies/popular/'
        return context
    
    def get_object(self):
        user = self.request.user
        exclude_ids = []
        if user.is_authenticated:
            exclude_ids = [x.object_id for x in user.rating_set.filter(active=True)]
        movie_id_options = Movie.objects.all().popular().exclude(id__in=exclude_ids).values_list('id', flat=True)[:250]
        return Movie.objects.filter(id__in=movie_id_options).order_by("?").first()
    
    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ['movies/snippet/infinite.html']
        return ['movies/infinite-view.html']


movie_popular_view = MoviePopularView.as_view()