from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class ThemeMiddleware(MiddlewareMixin):
    """
    Middleware to handle theme preferences (light/dark mode)
    """
    
    def process_request(self, request):
        # Get theme from session, URL parameter, or default
        theme = request.GET.get('theme')
        
        if theme and theme in settings.AVAILABLE_THEMES:
            # Store theme preference in session
            request.session['theme'] = theme
        elif 'theme' not in request.session:
            # Set default theme if not set
            request.session['theme'] = settings.DEFAULT_THEME
        
        # Make theme available in request
        request.theme = request.session.get('theme', settings.DEFAULT_THEME)
        
        return None

    def process_response(self, request, response):
        # Ensure theme is always available
        if not hasattr(request, 'theme'):
            request.theme = settings.DEFAULT_THEME
        return response 