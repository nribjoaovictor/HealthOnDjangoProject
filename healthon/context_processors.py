from django.conf import settings

def demo(request):
    return {"read_only_demo": settings.READ_ONLY_DEMO}
