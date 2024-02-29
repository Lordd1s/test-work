from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from settings import settings
from training_system import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.GetProducts.as_view()),
    path('products/buy/<str:pk>/', views.subscribe),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
