from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods

from ml import tasks as ml_tasks

from .models import Rating

@require_http_methods(['POST'])
def rate_movie_view(request):
    if not request.htmx:
        return HttpResponse("Not Allowed", status=400)
    object_id = request.POST.get('object_id')
    rating_value = request.POST.get("rating_value")
    if object_id is None or rating_value is None:
        response = HttpResponse("Skipping", status=200)
        response['HX-Trigger'] = 'did-skip-movie'
        return response
    user = request.user
    message = "You must <a href='/accounts/login'>login</a> to rate this."
    if user.is_authenticated:
        message = "<span class='bg-danger text-light py-1 px-3 rounded'>An error occured.</div>"
        ctype = ContentType.objects.get(app_label='movies', model='movie')
        rating_obj = Rating.objects.create(content_type=ctype, object_id=object_id, value=rating_value, user=user)
        if rating_obj.content_object is not None:
            total_new_suggestions = request.session.get("total-new-suggestions") or 0
            items_rated = request.session.get('items-rated') or 0
            items_rated += 1
            request.session['items-rated'] = items_rated
            print('items_rated', items_rated)
            if items_rated % 5 == 0:
                print("trigger new suggestions")
                users_ids = [user.id]
                ml_tasks.batch_users_prediction_task.apply_async(kwargs ={
                    "users_ids": users_ids,
                    "start_page": total_new_suggestions,
                    "max_pages": 10
                })
            message = "<span class='bg-success text-light py-1 px-3 rounded'>Rating saved!</div>"
            response = HttpResponse(message, status=200)
            response['HX-Trigger-After-Settle'] = 'did-rate-movie'
            return response
    return HttpResponse(message, status=200)