from django.urls import path
from kindle import views

urlpatterns = [
    path("", views.Ebookmainpage.as_view(), name="mainpage"),
    path("list/", views.Ebooklist.as_view(), name="list"),
    path("myself/", views.Myself.as_view(), name="myself"),
    path("search/", views.Search.as_view(), name="search"),
    path("noserve/", views.Nosearch.as_view(), name="noserve"),
    path("book/download/<str:id>/", views.Ebookdownload.as_view(), name="download"),
    path("book/star/<str:id>/", views.Ebookstar.as_view()),
    path("book/starajax/",views.Ebookstarjson.as_view()),
    path("book/<str:id>/", views.Ebookdetail.as_view(), name="detail"),
]