from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('review/', views.ReviewCreateView.as_view(), name='create_review'),
    path('review/<int:pk>/update', views.ReviewUpdateView.as_view(), name='update_review'),
    path('review/<int:pk>/delete', views.ReviewDeleteView.as_view(), name='delete_review'),
    path('review/<int:review_id>/like', views.like_view, {'route': 'like'}, name='like_review'),
    path('review/<int:review_id>/unlike', views.like_view, {'route': 'unlike'}, name='unlike_review'),
    path('gyms/<str:gym_name>/', views.GymDetailView.as_view(), name='gym_detail')
]