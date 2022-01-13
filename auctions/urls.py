from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listall", views.listall, name="listall"),
    path("newauction", views.newauction, name="newauction"),
    path("allcategories", views.allcategories, name="allcategories"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("following", views.following, name="following"),
    path("followadd", views.followadd, name="followadd"),
    path("followremove", views.followremove, name="followremove"),
    path("delivered", views.delivered, name="delivered"),
    path("deleted", views.deleted, name="deleted"),
    path("close", views.close, name="close"),
    path("closedauctions", views.closedauctions, name="closedauctions"),
    path("newcomment", views.newcomment, name="newcomment"),
    path("auction/<int:id>", views.auction, name="auction"),
    path("error", views.error, name="error")
]
