from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register),
    # path('login/',views.UserLoginView.as_view),
    path('login/',views.Login),
    #path('login/',views.UserLoginView.as_view()),
    path('logout/',views.Logout),
    path('Logout/',views.logout_page),
    path('dashboard/',views.dashboard),
    path('profile/',views.profile),
    path('transaction/',views.transaction),
    path('transfer/',views.FundTransfer),
    path('notifications/',views.notification),
]
