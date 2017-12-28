from django.conf.urls import url
from . import views          
urlpatterns = [
    url(r'^main$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^dashboard$', views.dash, name='dash'),
    url(r'^wish_items/create$', views.create_display, name='create_display'),
    url(r'^wish_items/add_new$', views.add_new_product, name='add_new_product'),
    url(r'^wish_items/(?P<product_id>\d+)$', views.product_display, name='product_display'),
    url(r'^add_to_wish/(?P<id>\d+)$', views.add_to_wish, name='add_to_wish'),
    url(r'^remove_from_wish/(?P<wish_id>\d+)$', views.remove_from_wish, name='remove_from_wish'),
    url(r'^delete/(?P<product_id>\d+)$', views.delete, name='delete')
]