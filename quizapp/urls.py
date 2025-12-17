from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Quiz application routes
    path("", include("quiz.urls")),
]
