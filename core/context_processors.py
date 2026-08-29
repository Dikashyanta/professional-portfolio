from .models import Profile


def profile_context(request):
    return {'profile': Profile.objects.first()}