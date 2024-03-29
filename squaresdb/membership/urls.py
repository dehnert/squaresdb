from django.conf.urls import url
from django.urls import path

from squaresdb.membership import views

membership_patterns = [ # pylint:disable=invalid-name
    url(r'^person/(\d+)/$', views.view_person, name='person'),
    url(r'^person/edit/$', views.edit_user_person, name='person-user-edit'),
    url(r'^person/edit/(\d+)/$', views.edit_user_person, name='person-user-edit-id'),
    url(r'^person/link/([A-Za-z0-9]+)/$', views.edit_person_personauthlink, name='person-link'),
    url(r'^link/bulk_create/', views.create_personauthlinks, name='personauthlink-bulkcreate'),
    url(r'^class/$', views.ClassList.as_view(), name='class-list'),
    path(r'class/<int:pk>/', views.ClassDetail.as_view(), name='class-detail'),
    url(r'^class/import/$', views.import_class, name='class-import'),
]

def urls():
    return (membership_patterns, 'membership', 'membership', )
