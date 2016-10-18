from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.template import loader
from django.shortcuts import render_to_response, render, get_object_or_404 

from django.core.context_processors import csrf

from django.conf import settings

from forms import submissionAssignmentForm, submissionForm, AssignmentForm, ArticleForm, UserForm # UserProfileForm
from .models import Article, Assignment, Solution 

from django.template import RequestContext
from django.contrib import auth

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


from sklearn import metrics, cross_validation

import numpy as np

import matplotlib.pyplot as plt

import datetime

from django.utils import timezone

from datetime import datetime, timedelta


from django.db.models import Max, Min

def computeSampledMetrics (predfile, solfile,samplesize,scoring_method):
    myPredFile = open (settings.MEDIA_ROOT + str(predfile), 'r')
    #myPredFile = open (settings.MEDIA_ROOT +  '/solution_files/sol.txt', 'r')
    myTrueFile = open (settings.MEDIA_ROOT + str(solfile), 'r')
    predictions = []
    ground      = []
    for predline in myPredFile:
        predictions.append(predline)
    for trueline in myTrueFile:
        ground.append(trueline)
    
    ground = np.array (ground)
    predictions= np.array (predictions)

    rs = cross_validation.ShuffleSplit (len(ground), n_iter=1, test_size=0.01 * samplesize, random_state=0)
    for train_index, test_index in rs:
        sample_ground       = ground [test_index]
        sample_predictions  = predictions [test_index]
        print np.mean (sample_ground == sample_predictions)    
        print metrics.classification_report (sample_ground, sample_predictions)
    #return metrics.f1_score (sample_ground,sample_predictions, pos_label=1)
        if scoring_method == 'RE':
            ytrue = np.array (sample_ground, dtype=np.float)
            ypred = np.array (sample_predictions, dtype=np.float)
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
        return 1.0 - metrics.mean_squared_error (ytrue, ypred)
    
   # return metrics.accuracy_score(sample_ground, sample_predictions) 
    


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


def computeMetrics (predfile, solfile, scoring_method):
    myPredFile = open (settings.MEDIA_ROOT + str(predfile), 'r')
    #myPredFile = open (settings.MEDIA_ROOT +  '/solution_files/sol.txt', 'r')
    myTrueFile = open (settings.MEDIA_ROOT + str(solfile), 'r')
    predictions = []
    ground      = []
    for predline in myPredFile:
        predictions.append(predline)
    for trueline in myTrueFile:
        ground.append(trueline)
    
    if len(predictions) != len(ground):
        return -100.0
    else:
        print np.mean (ground == predictions)    
        print metrics.classification_report (ground, predictions)
      
        if scoring_method == 'RE':
            ytrue = np.array (ground, dtype=np.float)
            ypred = np.array (predictions, dtype=np.float)
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
            return 1.0 - metrics.mean_squared_error (ytrue, ypred)



    


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
            print corr
    myPredFile.close()
    myTrueFile.close()

    return (1.0 * corr)/len(ground)



def index(request):
    
    form = ArticleForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('fileuploader/create_article.html',args)


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
        return render_to_response('loggedin.html',args)
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


@staff_member_required
def createAssignment (request):
    if request.POST:
        form = AssignmentForm (request.POST, request.FILES)
        if form.is_valid():
            a = form.save()
            return HttpResponseRedirect('viewAssignments.html')
    else:
        form = AssignmentForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('fileuploader/createAssignment.html',args)


@login_required
def viewErrorMessage(request,message):
    args = {}
    args['message'] = message
    args['user'] = request.user
    return render_to_response ('fileuploader/viewErrorMessage.html', args)





@login_required
def submitChosenAssignment (request,assignment_id):
    if request.POST:
        form = submissionAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            print a.user
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
            print len(obj2)
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
   return render_to_response ('fileuploader/thanksSubmissions.html') 


@staff_member_required
def viewSubmissions (request):
    args = {}
    args.update (csrf (request))
    args['solutions'] = Solution.objects.all ()
    return render_to_response ('fileuploader/viewSubmissions.html', args)


@login_required
def viewAssignments (request):
    args = {}
    args.update(csrf(request))
    args['assignments'] = Assignment.objects.all()
    #UTC TIME args['currenttime'] = datetime.datetime.now()
    args['currenttime'] = timezone.now()
    args['user'] = request.user
    return render_to_response('fileuploader/viewAssignments.html',args)


@staff_member_required
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
            print u
            i = i + 1
    leaderboard.sort(key = lambda x: x.score, reverse=True)

    args['submissions'] = leaderboard
    
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
            print u
            i = i + 1
    leaderboard.sort(key = lambda x: x.public_score, reverse=True)

    args['submissions'] = leaderboard
    
    return render (request, 'fileuploader/viewPublicRankings.html', args)  

#student view of Assignments 
#for download
#seeing his own submissions

@staff_member_required
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
    print current_user
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
    print fileurls
    args['fileurls'] = fileurls
    #plt.show ()
    return render (request, 'fileuploader/viewAssignmentsDetail.html', args)  


@staff_member_required
def deleteAssignment (request, assignment_id):
   if request.user.is_superuser: 
        obj2 = Solution.objects.filter (assignment = assignment_id).count()
        if obj2 > 0:
            u1 = Solution.objects.filter(assignment=assignment_id).delete()
    
        u2 = Assignment.objects.get(pk=assignment_id).delete()
        return render_to_response ('fileuploader/viewAssignments.html') 
   else:
        html = "<html><body>You are not authorized to permit this action</body></html>" 
        return HttpResponse(html)


@staff_member_required
def editAssignment (request,assignment_id):
    assignment  = get_object_or_404 (Assignment, pk = assignment_id)
    if request.POST:
        print "I am here"
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            a = form.save()
            print "Form is valid"
            #viewAssignmentsDetail (request, assignment_id)
            return HttpResponseRedirect('../../viewAssignments.html')

    else:
        form = AssignmentForm(instance=assignment)
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request, 'fileuploader/editAssignment.html',args)




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
        return render_to_response('fileuploader/create_article.html',args)

def register(request):
    if request.POST:
        uf = UserForm(request.POST, prefix='user')
        #upf= UserProfileForm(request.POST, prefix='userprofile')
        if uf.is_valid():
            user = uf.save()
            user.set_password(user.password)    
            user.save()

            #userprofile = upf.save(commit=False)
            #userprofile.user=user
            #userprofile.save()
            return HttpResponseRedirect('/fileuploader/login')
    else:
        uf = UserForm(prefix='user')
        #upf= UserProfileForm(prefix='userprofile')
    
    #return render_to_response('register.html', dict(userform=uf,userprofileform=upf), context_instance=RequestContext(request))
    return render_to_response('register.html', dict(userform=uf), context_instance=RequestContext(request))

#user = User.objects.create_user(username=request.POST['login'], password=request.POST['password'])



# Create your views here.
