#forms.py

from django import forms
from models import Solution, Article, Assignment
from django.contrib.auth.models import User
from models import UserProfile

class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ('title','fileshot')

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('name','description','ground_truth')


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
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        fields  = ['team_name']
