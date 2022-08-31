from .models import RatingChoice

def rating_choices(request):
    return {
        "rating_choices": RatingChoice.values
    }