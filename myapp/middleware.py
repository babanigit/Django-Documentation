# myapp/middleware.py

from django.http import JsonResponse
import re

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the /trial route
        if re.match(r'^/trial/?$', request.path):
            token = request.headers.get('Authorization')
            if token != 'Bearer your_token_here':  # Replace with your token validation
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        return self.get_response(request)
