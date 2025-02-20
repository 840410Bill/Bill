from django.shortcuts import redirect
from django.http import Http404, JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from .models import URLTransform
from django_ratelimit.decorators import ratelimit
from .utils import generate_short_code


@api_view(["POST"])
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def origin_url(request):
    original_url = request.data.get('original_url')

    if not original_url:
        return JsonResponse({
            "success": False,
            "reason": "Missing 'original_url'"
        }, status=400)
    
    valid = URLValidator()

    if len(original_url) > 2048:
        return JsonResponse({
            "success": False,
            "reason": "'Original_url' is too long."
        }, status=400)
    
    try:
        valid(original_url)
    except ValidationError:
        return JsonResponse({
            "success": False,
            "reason": "Invalid URL format"
        }, status=400)
    
    short_code = generate_short_code()
    expiration_date = timezone.now() + timedelta(days=30)
    URLTransform.objects.create(
        original_url=original_url,
        short_code=short_code,
        expiration_date=expiration_date
    )
    short_url = f"http://127.0.0.1:8000/api/r/{short_code}"
    return JsonResponse({
        "success": True,
        "short_url": short_url,
        "expiration_date": expiration_date.strftime('%Y-%m-%d %H:%M:%S')
    })

@api_view(["GET"])
def redirect_to_original_url(request, short_code):
    try:
        short_url_obj = URLTransform.objects.get(short_code=short_code)
        if short_url_obj.expiration_date < timezone.now():
            return JsonResponse({
                "success": False,
                "reason": "This short URL has expired."
            }, status=410)
        return redirect(short_url_obj.original_url)
    except URLTransform.DoesNotExist:
        raise Http404("Not Found")