from django import forms
from .models import People,Socials,Status,Projects
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField


 
class PersonForm(forms.ModelForm):
 
    class Meta:
        model = People
        fields = ['firstname','lastname','pronouns','handle','pID']
        labels = {
            "firstname": ("First Name"),
            "pID": ("Projects"),
        }
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['pID'].label_from_instance = self.label_from_instance
        self.fields['pID'].required = False
    @staticmethod
    def label_from_instance(obj):
        return obj.projectName
    
class SocialForm(forms.ModelForm):
 
    class Meta:
        model = Socials
        fields = ['twitter','youtube','twitch','website','email','other','image']
    def __init__(self, *args, **kwargs):
        super(SocialForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class ProjectForm(forms.ModelForm):
 
    class Meta:
        model = Projects
        fields = ['projectName','projectDescription']
        labels = {
            "projectName": ("Project Name"),
            'projectDescription': ("Project Description"),
        }
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['projectDescription'].required = False

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['approved','active']