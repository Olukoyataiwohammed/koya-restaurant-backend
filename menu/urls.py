from django.urls import path
from . import views

urlpatterns =[
    path("",view=views.categoryView),
    path("post-category/",view=views.add_category),
    path("menu-item/",view=views.list_menu_item),
    path("post-item/",view=views.add_item),
]

