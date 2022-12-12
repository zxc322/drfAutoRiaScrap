from django.urls import path
from . import views

urlpatterns = [
    path('scrap/page/<int:pk>', views.ScrapPage.as_view()),
    path('all_cars/', views.GetAllCars.as_view())
]
