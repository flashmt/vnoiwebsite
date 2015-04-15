import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings")
    from django.contrib.auth.models import User
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    user = User.objects.get(username=str(sys.argv[1]))
    profile = user.profile
    print profile.activation_key
