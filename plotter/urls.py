from django.urls import path
from . import views

urlpatterns = [
    path("", views.plot_page, name="home"),
    path("plot-image/", views.plot_image, name="plot_image"),
]
