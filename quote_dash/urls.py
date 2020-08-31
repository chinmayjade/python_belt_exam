from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.quotes),
    path('post_quote', views.postQuote), #post quote
    path('post_like', views.postLike), #post a like
    path('delete_quote', views.deleteQuote), #delete a quote
    path('user/<int:id>', views.viewUser),
    path('edit_account', views.editAccount),
    path('update_user', views.updateUser),
    path('logout', views.logout),
]