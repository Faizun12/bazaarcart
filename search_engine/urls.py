from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/search/', views.api_search, name='api_search'),
    path('store/bazaar/<int:product_id>/', views.bazaar_store, name='bazaar_store'),
    path('web-details/', views.web_details, name='web_details'),
]
