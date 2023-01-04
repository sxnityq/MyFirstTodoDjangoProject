from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


from .settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
