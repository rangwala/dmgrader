from django.http import HttpResponseRedirect,HttpResponse
from django.urls import *
from django.template import loader
from django.shortcuts import render_to_response, render, get_object_or_404

from django.template.context_processors import csrf

from django.conf import settings

from .forms import submissionAssignmentForm, submissionForm, AssignmentForm, ArticleForm, UserForm, CourseForm # UserProfileForm
from .models import Article, Assignment, Solution,  Course, Enrolled

from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required


from sklearn import metrics
from sklearn.model_selection import cross_val_score, ShuffleSplit

import numpy as np

import pdb

import matplotlib.pyplot as plt

import datetime

from django.utils import timezone

from datetime import datetime, timedelta


from django.db.models import Max, Min

from django.core.exceptions import PermissionDenied

def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied           
        return function(request, *args, **kwargs)
    return _inner

def superuser_or_staff(function):
    def _inner(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied           
        return function(request, *args, **kwargs)
    return _inner


def computeSampledMetrics (predfile, solfile,samplesize,scoring_method):
    myPredFile = open (settings.MEDIA_ROOT + str(predfile), 'r')
    #myPredFile = open (settings.MEDIA_ROOT +  '/solution_files/sol.txt', 'r')
   
    myTrueFile = open (settings.MEDIA_ROOT + str(solfile), 'r')
    #myPredFile = open (str(predfile), 'r')
    #myTrueFile = open (str(solfile), 'r')
    predictions = []
    ground      = []
    for predline in myPredFile:
        predictions.append(predline)
    for trueline in myTrueFile:
        ground.append(trueline)

    ground = np.array (ground)
    predictions= np.array (predictions)
    rs = ShuffleSplit (n_splits=1, test_size=0.01 * samplesize, random_state=0)
    for train_index, test_index in rs.split(ground):
        sample_ground       = ground [test_index]
        sample_predictions  = predictions [test_index]
        #print np.mean (sample_ground == sample_predictions)
        #print metrics.classification_report (sample_ground, sample_predictions)
        #return metrics.f1_score (sample_ground,sample_predictions, pos_label=1)
        if scoring_method == 'RE' or scoring_method == 'RC':
            ypred = np.array (sample_predictions, dtype=np.float)
            if scoring_method == 'RE':
                ytrue = np.array (sample_ground, dtype=np.float)
            else:
                ytrue = np.array (sample_ground,dtype=np.int)
        else:
            ytrue = np.array(sample_ground,dtype=np.int)
            ypred = np.array(sample_predictions,dtype=np.int)

    if scoring_method == 'F1':
        return metrics.f1_score(ytrue,ypred,pos_label=1)
    if scoring_method == 'AC':
        return metrics.accuracy_score(ytrue, ypred)
    if scoring_method == 'V1':
        return metrics.v_measure_score(ytrue, ypred)
    if scoring_method == 'RE':
        return  metrics.mean_squared_error (ytrue, ypred) ** 0.5
    if scoring_method == 'RC':
        return metrics.roc_auc_score (ytrue, ypred)

   # return metrics.accuracy_score(sample_ground, sample_predictions)

@login_required
def indexCourse(request):
    args = {}
    args['user'] = request.user
    args['courses'] = request.user.course_set.all()
    return render_to_response('fileuploader/courses.html', args)

@superuser_or_staff
def newCourse(request):
    form = CourseForm()
    args = {}
    args.update(csrf(request))
    args['user'] = request.user
    args['form'] = form
    return render_to_response('fileuploader/newcourse.html', args)

@superuser_or_staff
def createCourse(request):
    form = CourseForm(request.POST)
    if form.is_valid():
        a = form.save()
        return HttpResponseRedirect('courses.html')
    else:
        args = {}
        args.update(csrf(request))
        args['form'] = form
        args['user'] = request.user
        return render_to_response('fileuploader/newcourse.html', args)

@superuser_or_staff
def editCourse(request, course_id):
    course = Course.objects.filter(id=course_id).first()
#    if  course in request.user.course_set():
    form = CourseForm()
    args = {}
    args.update(csrf(request))
    args['user'] = request.user
    args['course'] = course
    args['form'] = form
    return render_to_response('fileuploader/editCourse.html', args)
   # else:
   #     return HttpResponseRedirect('/fileuploader/login/')
    
def updateCourse(request, course_id):
    course = Course.objects.filter(id=course_id).first()
    form = CourseForm(request.POST, instance=course)
    if form.is_valid():
        a = form.save()
        return HttpResponseRedirect('/fileuploader/courses')
    else:
        args = {}
        args.update(csrf(request))
        args['form'] = form
        args['user'] = request.user
        args['course'] = course
        return render(request, 'fileuploader/editCourse.html',args)

    """
    corr = 0
    for i in range (len(ground)):
        if (ground[i] == predictions[i]):
            corr = corr+1;
            print corr
    myPredFile.close()
    myTrueFile.close()

    return (1.0 * corr)/len(ground)

"""

#@login_required
def computeMetrics (predfile, solfile, scoring_method):
    
    myPredFile = open (settings.MEDIA_ROOT + str(predfile), 'r')
    #myPredFile = open (settings.MEDIA_ROOT +  '/solution_files/sol.txt', 'r')
    myTrueFile = open (settings.MEDIA_ROOT + str(solfile), 'r')
    #myPredFile = open (str(predfile), 'r')

    
    #pdb.set_trace()
    predictions = []
    ground      = []
    for predline in myPredFile:
        predictions.append(predline)
    for trueline in myTrueFile:
        ground.append(trueline)

    if len(predictions) != len(ground):
        return -100.0
    else:
        #print np.mean (ground == predictions)
        #print metrics.classification_report (ground, predictions)
        print ("Hi")
        if scoring_method == 'RE' or scoring_method == 'RC':
            ypred = np.array (predictions, dtype=np.float)
            if scoring_method == 'RE':
                ytrue = np.array (ground, dtype=np.float)
            else:
                ytrue = np.array (ground, dtype=np.int)
        else:
            ytrue = np.array(ground,dtype=np.int)
            ypred = np.array(predictions,dtype=np.int)

        if scoring_method == 'F1':
            return metrics.f1_score(ytrue,ypred,pos_label=1)
        if scoring_method == 'AC':
            return metrics.accuracy_score(ytrue, ypred)
        if scoring_method == 'V1':
            return metrics.v_measure_score(ytrue, ypred)
        if scoring_method == 'RE':
            return  metrics.mean_squared_error (ytrue, ypred) ** 0.5
        if scoring_method == 'RC':
            return metrics.roc_auc_score (ytrue, ypred)





    """
    corr = 0
    for i in range (len(ground)):
        if (ground[i] == predictions[i]):
            corr = corr+1;
            print corr
    myPredFile.close()
    myTrueFile.close()

    return (1.0 * corr)/len(ground)

"""

@login_required
@superuser_only
def indexUser(request):
    args = {}
    args["user"] = request.user
    args["users"] = User.objects.all()
    return render_to_response('users.html',args)
    


def get_accuracy_value (filename):
    myPredFile = open (settings.MEDIA_ROOT + str(filename), 'r')
    #myPredFile = open (settings.MEDIA_ROOT +  '/solution_files/sol.txt', 'r')
    myTrueFile = open (settings.MEDIA_ROOT + '/solution_files/sol.txt', 'r')
    predictions = []
    ground      = []
    for predline in myPredFile:
        predictions.append(predline)
    for trueline in myTrueFile:
        ground.append(trueline)
    corr = 0
    for i in range (len(ground)):
        if (ground[i] == predictions[i]):
            corr = corr+1;
            #print corr
    myPredFile.close()
    myTrueFile.close()

    return (1.0 * corr)/len(ground)


@login_required
def index(request):

    form = ArticleForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('fileuploader/create_article.html',args)

@login_required
def articles(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/fileuploader/login/')

    #username = request.POST.get('username')
    #password = request.POST.get('password')
    #user = authenticate(username=username, password=password)


    args = {}
    args.update(csrf(request))
    args['articles'] = Article.objects.all()
    return render_to_response('fileuploader/articles.html',args)


#def login(request,user):


def login (request):
    c={}
    c.update(csrf(request))
    return render_to_response('login.html',c)

def auth_view (request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user     = auth.authenticate(username=username, password=password)
    #print user, username, password
    if user is not None:
        auth.login(request,user)
        args={}
        args.update(csrf(request))
        args['user'] = user
        return HttpResponseRedirect('/fileuploader/loggedin', args)
    else:
        return HttpResponseRedirect('/fileuploader/invalid')

@login_required
def loggedin(request):
    args = {}
    args.update (csrf (request))
    args['user'] = request.user
    return render_to_response('loggedin.html', args)

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    auth.logout(request)
    return render_to_response('logout.html')



def computescores (request):
    args = {}
    args.update(csrf(request))
    #args['articles'] = Article.objects.filter(title='aaa').update(accuracy=get_accuracy_value(Article.fileshot.filename))
    obj1 = Article.objects.filter(accuracy=0.0)
    for items in obj1:
        items.accuracy = get_accuracy_value (items.fileshot)
        items.save()

    args['articles'] = obj1
    return render_to_response('fileuploader/computescores.html', args)

# this is only allowable by the ADMIN/INSTRUCTOR


@superuser_or_staff
def createAssignment (request):
    if request.POST:
        form = AssignmentForm (request.POST, request.FILES)
        if form.is_valid():
            form.instance.user_id = request.user.id
            a = form.save()
            return HttpResponseRedirect('viewAssignments.html')
        else:
            args = {}
            args.update(csrf(request))
            args['form'] = form
            args['user'] = request.user
            args['courses'] = request.user.course_set.all()
            return render_to_response('fileuploader/createAssignment.html', args)
    else:
        form = AssignmentForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        args['user'] = request.user
        args['courses'] = request.user.course_set.all()
        return render_to_response('fileuploader/createAssignment.html',args)


@login_required
def viewErrorMessage(request,message):
    args = {}
    args['message'] = message
    args['user'] = request.user
    return render_to_response ('fileuploader/viewErrorMessage.html', args)

# getter for user edit form
# renders the user in question information 
# that is editable via a form
# form submits to updateUser method
@superuser_only
def editUser(request, user_id):
    args = {}
    args.update(csrf(request))
    editable = User.objects.filter(id = user_id).first()
    args['user'] = request.user
    args['editable'] = editable
    return render_to_response('editUser.html',args)

# setter for user edit form
# renders the user in question information 
# that is editable via a form
# form submits to updateUser method
@superuser_only
def updateUser(request, user_id):
    editable = User.objects.filter(id = user_id).first()
    if request.POST.get('user-is_superuser'):
        editable.is_superuser = True
        editable.save()
    else:
        editable.is_superuser = False
        editable.save()
    
    if request.POST.get('user-is_staff'):
        editable.is_staff = True
        editable.save()
    else:
        editable.is_staff = False
        editable.save()
    return HttpResponseRedirect('/users.html')

@login_required
def submitChosenAssignment (request,assignment_id):
    if request.POST:
        form = submissionAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            #print a.user
            assignment  = get_object_or_404 (Assignment, pk = assignment_id)
            if timezone.now() > assignment.deadline_date:
                htmlmessage = "Past Deadline Date"
                args = {}
                args.update (csrf (request))
                args['message'] = htmlmessage
                args['user']    = request.user
                return render_to_response ('fileuploader/viewErrorMessage.html',args)


            min_dt = timezone.now () - timedelta (hours=24)
            max_dt = timezone.now()
            previous_today = Solution.objects.filter(assignment=assignment_id,user=a.user,status='OK',submission_time__range = (min_dt,max_dt)).count() #submission_time > (timezone.now()-timedelta(1)))

            if previous_today >= assignment.num_subs_per_day:
                htmlmessage = "You have already submitted the allowed submissions in a 24-hour cycle"
                args = {}
                args.update (csrf (request))
                args['message'] = htmlmessage
                args['user']    = request.user
                return render_to_response ('fileuploader/viewErrorMessage.html',args)

            truthFile = assignment.ground_truth

            a.assignment = assignment
            a.save()
            # update the counter
            # also update the score
            obj1 = Assignment.objects.get(pk = a.assignment_id) #.update(uploaded_cnt = uploaded_cnt + 1)
            truthFile = obj1.ground_truth
            scorer = obj1.scoring_method
            obj1.uploaded_cnt = obj1.uploaded_cnt + 1
            counter = obj1.uploaded_cnt
            obj1.save()
            # gets all the files back...
            # we need a table of student - attempts - etc

            obj2 = Solution.objects.filter (assignment = a.assignment)
            #print len(obj2)
            for items in obj2:
                if items.solution_file == a.solution_file:
                    items.attempt = counter
                    items.score =       computeMetrics (items.solution_file, truthFile,scorer)
                    flag_save = 1
                    if items.score == -100:
                        htmlmessage = "Your Prediction File has incorrect number of entries"
                        args = {}
                        args.update (csrf (request))
                        args['message'] = htmlmessage
                        args['user'] = request.user
                        return render_to_response ('fileuploader/viewErrorMessage.html',args)

                        #return HttpResponse(htmlmessage)
                    else:
                        items.submission_time = timezone.now()
                        items.status = 'OK'
                        #Compute the Public_SCORE
                        items.public_score = computeSampledMetrics (items.solution_file, truthFile, obj1.sampling_private,scorer)
                        items.save()
            pdb.set_trace()
            args={}
            args.update (csrf (request))
            #create a splash page
            args['user'] = request.user
            return render_to_response('fileuploader/thanksSubmissions.html',args)
            #return render_to_response('fileuploader/viewSubmissions.html',args)
    else:
        assignment  = get_object_or_404 (Assignment, pk = assignment_id)
        form = submissionAssignmentForm()
        args = {}
        args.update(csrf (request))
        args['form'] = form
        args['assignment'] = assignment
        args['user'] = request.user
        #return HttpResponseRedirect('viewSubmissions.html')
        return render_to_response('fileuploader/submitChosenAssignment.html',args)




#@login_required
#def submitAssignment (request):
#    if request.POST:
#        form = submissionForm(request.POST, request.FILES)
#        if form.is_valid():
#            a = form.save(commit=False)
#            a.user = request.user
#            print a.user
#            a.save()
            # update the counter
            # also update the score
#            obj1 = Assignment.objects.filter(name = a.assignment) #.update(uploaded_cnt = uploaded_cnt + 1)
#            for items in obj1:
#                items.uploaded_cnt = items.uploaded_cnt + 1
#                counter = items.uploaded_cnt
#                truthFile = items.ground_truth
#                items.save()
            # gets all the files back...
            # we need a table of student - attempts - etc

#            obj2 = Solution.objects.filter (assignment = a.assignment)

#            for items in obj2:
#                if items.solution_file == a.solution_file:
#                    items.attempt = counter
#                    items.score = computeMetrics (items.solution_file, truthFile)
#                    items.save()
#            return HttpResponseRedirect('viewSubmissions.html')
#    else:
#        form = submissionForm()
#        args = {}
#        args.update(csrf (request))
#        args['form'] = form
#        return render_to_response('fileuploader/submitAssignment.html',args)
#'''

def thanksSubmissions (request):
   args['user'] = request.user
   return render_to_response ('fileuploader/thanksSubmissions.html', args)


@superuser_or_staff
def viewSubmissions (request):
    args = {}
    args.update (csrf (request))
    args['solutions'] = Solution.objects.all()
    args['user'] = request.user
    return render_to_response ('fileuploader/viewSubmissions.html', args)

@login_required
def selectCourse (request):
    if request.POST:
        form = CourseForm (request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            return HttpResponseRedirect('viewAssignments.html')
    else:
        form = CourseForm()
        args = {}
        args.update(csrf(request))

        args['opts'] = Course.objects.values_list('classnum', flat=True)
        args['user'] = request.user
        return render_to_response('fileuploader/selectCourse.html',args)





@superuser_or_staff
def viewAssignments (request):
    args = {}
    args.update(csrf(request))
    current_user = request.user
    sc=Course.objects.filter(user=current_user)
    if current_user.is_superuser:
        args['assignments'] = Assignment.objects.all()
    elif current_user.is_staff:
        args['assignments'] = current_user.assignment_set.all()
    else:
        return HttpResponseRedirect('../../my_assignments.html')


    #UTC TIME args['currenttime'] = datetime.datetime.now()
    args['currenttime'] = timezone.now()
    args['user'] = request.user
    return render_to_response('fileuploader/viewAssignments.html',args)

@login_required
def myAssignments (request):
    args = {}
    args.update(csrf(request))
    current_user = request.user
    args['user'] = current_user
    courses = Course.objects.filter(id__in = Enrolled.objects.filter(user = current_user).values('course_id'))
    assignments = Assignment.objects.filter(course_id__in = courses)
    args['assignments'] = assignments
    args['today'] = timezone.now()
    return render_to_response('fileuploader/myAssignments.html',args)

@login_required
def selectEnroll(request):
    args = {}
    args.update(csrf(request))
    current_user = request.user
    args['user'] = current_user
    allCourses = Course.objects.filter(year = timezone.now().year)
    myCourses = Course.objects.filter(id__in=Enrolled.objects.filter(user = current_user).values('course'))
    leftCourses = allCourses.difference(myCourses)
    args['courses'] = leftCourses
    return render_to_response('fileuploader/selectEnroll.html',args)

@login_required
def submitEnroll(request):
    if request.POST.get('course'):
        Enrolled.objects.create(course_id = request.POST.get('course'), user_id = request.user.id)
        return HttpResponseRedirect('/fileuploader/myAssignments.html')
    else:
        return HttpResponseRedirect('/fileuploader/selectEnroll.html')

@superuser_or_staff
def viewPrivateRankings (request, assignment_id):
    args = {}
    args.update (csrf (request))
    assignment = get_object_or_404 (Assignment, pk = assignment_id)
    args ['assignment'] = assignment
    subset_entries = Solution.objects.filter (assignment=assignment_id).filter(status = "OK").order_by('user','-submission_time')
    u = "None"
    leaderboard = []
    i = 0
    for entry in subset_entries:
        if entry.user != u:
            u = entry.user
            leaderboard.append(entry)
            i = i + 1
    if assignment.scoring_method == 'RE':
        leaderboard.sort(key = lambda x: x.score)
    else:
        leaderboard.sort(key = lambda x: x.score, reverse=True)

    args['submissions'] = leaderboard
    args['user'] = request.user

    return render (request, 'fileuploader/viewPrivateRankings.html', args)




#student view
@login_required
def viewPublicRankings (request, assignment_id):
    args = {}
    args.update (csrf (request))
    assignment = get_object_or_404 (Assignment, pk = assignment_id)
    args ['assignment'] = assignment
    subset_entries = Solution.objects.filter (assignment=assignment_id).filter(status = "OK").order_by('user','-submission_time')
    u = "None"
    leaderboard = []
    i = 0
    for entry in subset_entries:
        if entry.user != u:
            u = entry.user
            leaderboard.append(entry)
            i = i + 1
    if assignment.scoring_method == 'RE':
        leaderboard.sort(key = lambda x: x.public_score)
    else:
        leaderboard.sort(key = lambda x: x.public_score, reverse=True)
    args['submissions'] = leaderboard
    args['user'] = request.user
    return render (request, 'fileuploader/viewPublicRankings.html', args)

    return render (request, 'fileuploader/viewPublicRankings.html', args)

#student view of Assignments
#for download
#seeing his own submissions

@superuser_or_staff
def viewSubmissionLogs (request, assignment_id):
    args = {}
    args.update (csrf (request))
    assignment = get_object_or_404 (Assignment, pk = assignment_id)
    args ['assignment'] = assignment

    args['user'] = request.user

    args['submissions'] = Solution.objects.filter (assignment = assignment_id,status='OK').order_by('submission_time')

    scores_so_far = Solution.objects.values_list('score').filter (assignment = assignment_id,status='OK').order_by('submission_time')
    pub_scores_so_far = Solution.objects.values_list('public_score').filter (assignment = assignment_id,status='OK').order_by('submission_time')
    #print np.array (scores_so_far)
    plt.plot (np.array(scores_so_far), 'ro')
    plt.plot (np.array(pub_scores_so_far), 'b*')
    pngfilename =  str('test' + assignment_id + '.png')
    plt.savefig(settings.MEDIA_ROOT + pngfilename)
    args['figplot'] = pngfilename


    return render (request, 'fileuploader/viewSubmissionLogs.html', args)


@login_required
def viewAssignmentsDetail (request,assignment_id):
    args = {}
    args.update (csrf (request))
    assignment  = get_object_or_404 (Assignment, pk = assignment_id)
    args['assignment'] = assignment
    current_user = request.user
    args['user'] = current_user
    args['submissions'] = Solution.objects.filter (assignment = assignment_id,user=current_user).order_by('-submission_time')

    '''
    # create a plot
    scores_so_far = Solution.objects.values_list('score').filter (assignment = assignment_id)
    #print np.array (scores_so_far)
    plt.plot (np.array(scores_so_far), 'ro')


    pngfilename =  str('test' + assignment_id + '.png')
    plt.savefig(settings.MEDIA_ROOT + pngfilename)
    args['figplot'] = pngfilename
    '''
    fileurls = settings.MEDIA_URL
    args['fileurls'] = fileurls
    #plt.show ()
    return render (request, 'fileuploader/viewAssignmentsDetail.html', args)


@superuser_or_staff
def deleteAssignment (request, assignment_id):
   args = {}
   args['user'] = request.user
   if request.user.is_superuser:
        obj2 = Solution.objects.filter (assignment = assignment_id).count()
        if obj2 > 0:
            u1 = Solution.objects.filter(assignment=assignment_id).delete()

        u2 = Assignment.objects.get(pk=assignment_id).delete()
        return HttpResponseRedirect('../../viewAssignments.html')
   else:
        html = "<html><body>You are not authorized to permit this action</body></html>"
        return HttpResponse(html)


@superuser_or_staff
def editAssignment (request,assignment_id):
    assignment  = get_object_or_404 (Assignment, pk = assignment_id)
    if request.POST:
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            a = form.save()
            #viewAssignmentsDetail (request, assignment_id)
            return HttpResponseRedirect('../../viewAssignments.html')
        else:
            args = {}
            args.update(csrf(request))
            args['form'] = form
            args['user'] = request.user
            return render(request, 'fileuploader/editAssignment.html',args)

    else:
        form = AssignmentForm(instance=assignment)
        args = {}
        args.update(csrf(request))
        args['form'] = form
        args['user'] = request.user
        return render(request, 'fileuploader/editAssignment.html',args)



@login_required
def create(request):
    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            a =  form.save()
            return HttpResponseRedirect('/fileuploader/articles.html')
    else:
        form = ArticleForm()

        args = {}
        args.update(csrf(request))
        args['form'] = form
        args['user'] = request.user
        return render_to_response('fileuploader/create_article.html',args)

def register(request):
    if request.POST:
        uf = UserForm(request.POST, prefix='user')
        if uf.is_valid():
            cuser = uf.save()
            cuser.set_password(cuser.password)
            cuser.save()
            return HttpResponseRedirect('/fileuploader/selectCourse.html')
    else:
        return render(request, 'register.html')

#user = User.objects.create_user(username=request.POST['login'], password=request.POST['password'])



