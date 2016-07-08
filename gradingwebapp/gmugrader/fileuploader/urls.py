from django.conf.urls import url,patterns,include

from django.conf.urls.static import static

from . import views

app_name='fileuploader'
urlpatterns=[
    url(r'^login/$', views.login, name ='login'),
    url(r'^auth/$', views.auth_view, name='auth_view'),
    url(r'^logout$',views.logout_page, name='logout_page'),
    url(r'^invalid$', views.invalid_login, name='invalid_login'),
    url(r'^loggedin$', views.loggedin,name='loggedin'),
    url(r'^$',views.index, name='index'),
    url(r'^create$',views.create, name='create'),
    url(r'^articles$',views.articles, name='articles'),
    url(r'^articles.html$',views.articles, name='articles'),
    url(r'^computescores.html$',views.computescores, name='computescores'),
    url(r'^register$',views.register, name='register'),
    url(r'^register.html$',views.register, name='register'),
    url(r'^createAssignment$', views.createAssignment, name='createAssignment'),
    url(r'^createAssignment.html$', views.createAssignment, name='createAssignment'),
    url(r'^\/viewAssignments.html$', views.viewAssignments, name='viewAssignments'),
    url(r'^viewAssignments.html$', views.viewAssignments, name='viewAssignments'),
    url(r'^\/viewAssignmentsDetail\/(?P<assignment_id>.*)\/$', views.viewAssignmentsDetail, name='viewAssignmentsDetail'),
    url(r'^\/viewAssignmentsDetail\/(?P<assignment_id>.*)\/edit$', views.editAssignment, name='editAssignment'),
    url(r'^\/viewAssignmentsDetail\/(?P<assignment_id>.*)\/delete$', views.deleteAssignment, name='deleteAssignment'),
    url(r'^submitChosenAssignment\/(?P<assignment_id>.*)\/$', views.submitChosenAssignment, name='submitChosenAssignment'),
    url(r'^submitAssignment.html$', views.submitAssignment, name='submitAssignment'),
    url(r'^submitAssignment$', views.submitAssignment, name='submitAssignment'),
    url(r'^viewSubmissions.html$', views.viewSubmissions, name='viewSubmissions'),
    url(r'^viewSubmissions$', views.viewSubmissions, name='viewSubmissions'),
    url(r'^thanksSubmissions.html$', views.thanksSubmissions, name='thanksSubmissions'),
    url(r'^thanksSubmissions$', views.thanksSubmissions, name='thanksSubmissions'),
]   
