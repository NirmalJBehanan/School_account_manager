from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that don't require authentication
        public_urls = [
            reverse('login'),
            reverse('index'),
            reverse('about'),
            reverse('contact'),
            reverse('home'),
            '/static/',
            '/media/',
        ]

        # Check if the current URL is public
        if not any(request.path.startswith(url) for url in public_urls):
            if 'login_id' not in request.session:
                messages.error(request, 'Your session has expired. Please login again.')
                return redirect('login')

            # Update session expiry on each request
            request.session.modified = True

        response = self.get_response(request)
        return response 