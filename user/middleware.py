# user/middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import Profile

class EnsureProfileMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                request.user.profile
            except Profile.DoesNotExist:
                Profile.objects.create(user=request.user)
