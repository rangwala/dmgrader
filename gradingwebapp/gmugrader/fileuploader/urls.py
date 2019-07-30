from django.conf.urls import url,include

from django.conf.urls.static import static



from . import views

app_name='fileuploader'
urlpatterns=[
    url(r'^$', views.login, name ='login'),
    url(r'^login/?$', views.login, name ='login'),
    url(r'^auth/?$', views.auth_view, name='auth_view'),
    url(r'^logout$',views.logout_page, name='logout_page'),
    url(r'^logout/?$',views.logout_page, name='logout_page'),
    url(r'^invalid$', views.invalid_login, name='invalid_login'),
    url(r'^loggedin$', views.loggedin,name='loggedin'),
    url(r'^$',views.index, name='index'),
    url(r'^create$',views.create, name='create'),
    url(r'^articles$',views.articles, name='articles'),
    url(r'^articles.html$',views.articles, name='articles'),
    url(r'^computescores.html$',views.computescores, name='computescores'),
    url(r'^register$',views.register, name='register'),
    url(r'^register.html$',views.register, name='register'),
    
    url(r'^courses.html$',views.indexCourse, name='courses'),
    url(r'^courses$',views.indexCourse, name='courses'),
    url(r'^newcourse.html$',views.newCourse, name='newcourse'),
    url(r'^newcourse$',views.newCourse, name='newcourse'),
    url(r'^createCourse$',views.createCourse, name='createcourse'),
    url(r'^createCourse.html$',views.createCourse, name='createcourse'),

    url(r'^selectCourse$', views.selectCourse, name='selectcourse'),
    url(r'^selectCourse.html$', views.selectCourse, name='selectcourse'),
    url(r'^createAssignment$', views.createAssignment, name='createAssignment'),
    url(r'^createAssignment.html$', views.createAssignment, name='createAssignment'),
    url(r'^\/viewAssignments.html$', views.viewAssignments, name='viewAssignments'),
    url(r'^viewAssignments.html$', views.viewAssignments, name='viewAssignments'),
    url(r'^myAssignments.html$', views.myAssignments, name='myAssignments'),
    url(r'^myAssignments$', views.myAssignments, name='myAssignments'),
    url(r'^selectEnroll.html$', views.selectEnroll, name='selectEnroll'),
    url(r'^selectEnroll$', views.selectEnroll, name='selectEnroll'),
    url(r'^submitEnroll.html$', views.submitEnroll, name='submitEnroll'),
    url(r'^submitEnroll$', views.submitEnroll, name='submitEnroll'),

    url(r'^courses\/(?P<course_id>.*)\/edit$', views.editCourse, name='editCourse'),
    url(r'^updateCourse\/(?P<course_id>.*)$', views.updateCourse, name='updateCourse'),
    
    url(r'^viewErrorMessage.html$', views.viewErrorMessage, name='viewErrorMessage'),
    url(r'^viewSubmissionLogs\/(?P<assignment_id>.*)\/?$', views.viewSubmissionLogs, name='viewSubmissionLogs'),
    url(r'^viewPrivateRankings\/(?P<assignment_id>.*)\/?$', views.viewPrivateRankings, name='viewPrivateRankings'),
    url(r'^viewPublicRankings\/(?P<assignment_id>.*)\/?$', views.viewPublicRankings, name='viewPublicRankings'),
    url(r'^viewAssignmentsDetail\/(?P<assignment_id>.*)\/?$', views.viewAssignmentsDetail, name='viewAssignmentsDetail'),
    url(r'^editAssignment\/(?P<assignment_id>.*)\/edit$', views.editAssignment, name='editAssignment'),
    url(r'^deleteAssignment\/(?P<assignment_id>.*)\/delete$', views.deleteAssignment, name='deleteAssignment'),
    url(r'^submitChosenAssignment\/(?P<assignment_id>.*)\/?$', views.submitChosenAssignment, name='submitChosenAssignment'),
    #url(r'^submitAssignment.html$', views.submitAssignment, name='submitAssignment'),
    #url(r'^submitAssignment$', views.submitAssignment, name='submitAssignment'),
    url(r'^viewSubmissions.html$', views.viewSubmissions, name='viewSubmissions'),
    url(r'^viewSubmissions$', views.viewSubmissions, name='viewSubmissions'),
    url(r'^thanksSubmissions.html$', views.thanksSubmissions, name='thanksSubmissions'),
    url(r'^thanksSubmissions$', views.thanksSubmissions, name='thanksSubmissions'),
    
    
]
