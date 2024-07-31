
from django import forms
from .models import Course,Solution, Article, Assignment
from django.contrib.auth.models import User

#tinymce editor
#from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

from django.utils import timezone



from datetimewidget.widgets import DateTimeWidget

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title','fileshot')

class AssignmentForm(forms.ModelForm):
    #description  = forms.CharField(widget=TinyMCE(attrs={'cols':80, 'rows': 40} ))
    #deadline_date = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    #samping_private=forms.IntegerField(label='1-100')
    class Meta:
        model = Assignment
        fields = ('name','description','ground_truth','deadline_date','test_data','train_data','format_example','num_subs_per_day','hidden_status','scoring_method','sampling_private', 'course')

class submissionAssignmentForm (forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['solution_file']



class submissionForm (forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('assignment','solution_file')



class UserForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_superuser', 'is_staff']

class CourseForm (forms.ModelForm):
    class Meta:
        model = Course
        fields = ['classnum', 'name', 'section', 'year', 'semester', 'description', 'user']


'''
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        fields  = ['class_name']
'''
