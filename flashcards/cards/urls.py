from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("card/next", views.next_card, name="next_card"),
    path('card/<int:card_id>', views.guess_card , name = 'guess_card')

]