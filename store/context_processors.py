from django.conf import settings

def theme_processor(request):
    """
    Context processor to make theme and language info available in all templates
    """
    return {
        'current_theme': getattr(request, 'theme', settings.DEFAULT_THEME),
        'available_themes': settings.AVAILABLE_THEMES,
        'available_languages': settings.LANGUAGES,
        'current_language': getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE),
    } 