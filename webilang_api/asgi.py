#
# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webilang_api.settings')
#
# application = get_asgi_application()

import os
import django

from channels.routing import get_default_application #
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webilang_api.settings')
django.setup()
application = get_default_application()