from django.urls import path
from webapp.views import *

urlpatterns = [
    path('review/', ReviewView.as_view(), name='review'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('review/add/',  ReviewCreateView.as_view(), name='review_add'),
    path('review/<int:pk>/edit/',  ReviewUpdate.as_view(), name='update_review'),
    path('review/<int:pk>/delete/', DeleteReview.as_view(), name='delete_review'),
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdate.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='delete_product'),
]

app_name = 'webapp'
