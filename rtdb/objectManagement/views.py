from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import People, Projects,Socials,Status
from django import forms
from django.template import RequestContext
from django.contrib import messages
from django.contrib.messages import get_messages
from .forms import PersonForm,SocialForm,ProjectForm,StatusForm
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

#Tests
def moderatorCheck(user):
    return user.is_staff

def adminCheck(user):
    return user.is_staff
# Create your views here.

def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def list(request,detailType):
  match detailType:
    case "person":
      if moderatorCheck(request.user):
        allPeople = People.objects.filter()
      else:
        allPeople = People.objects.filter(personStatus__approved=True)
      template = loader.get_template('people/peopleList.html')
      context = {
        'allPeople': allPeople,
        'messages': get_messages(request)
      }
      return HttpResponse(template.render(context,request))
    case "project":
      if moderatorCheck(request.user):
        allProjects = Projects.objects.filter()
      else:
        allProjects = Projects.objects.filter(projectStatus__approved=True)
      template = loader.get_template('projects/projectList.html')
      context = {
        'allProjects': allProjects,
        'messages': get_messages(request)
      }
      return HttpResponse(template.render(context,request))
    
def details(request,detailType,id):
  match detailType:
     case "person":
      template = loader.get_template('people/person.html')
      try:
        individualPerson = People.objects.get(hID=id)
      except People.DoesNotExist:
        messages.error(request,'Person does not exist')
        redirect('/list/person')
          
      try:
        personProjects = Projects.objects.get(pID=id)
      except Projects.DoesNotExist:
        personProjects = None

      context = {
      'person': individualPerson,
      'projects': individualPerson.pID.all(),
      'socialMedia': individualPerson.sID.getLinks
      }
      return HttpResponse(template.render(context, request))
     
     case "project":
      template = loader.get_template('projects/project.html')
      try:
        individualProject = Projects.objects.get(pk=id)
      except People.DoesNotExist:
        messages.error(request,'Project does not exist')
        return redirect('/list/project')
      
      context = {
        'project': individualProject,
        'socials': individualProject.sID.getLinks,
        'people': People.objects.filter(personStatus__approved=False,pID=individualProject)
      }
      return HttpResponse(template.render(context))

@login_required   
def editPerson(request,id=None):
  try:
    hInstance=get_object_or_404(People,pk=id)
  except:
    hInstance=None
  if request.method == 'POST':
    if hInstance==None:
      hInstance=People()
      hInstance.sID=Socials()
      hInstance.personStatus=Status()
      hInstance.personStatus.save()
      hInstance.sID.save()
      hInstance.save()      
    hForm = PersonForm(request.POST,instance=hInstance,prefix="hForm")
    sForm = SocialForm(request.POST,request.FILES,instance=hInstance.sID,prefix="sForm")
    if moderatorCheck(request.user):
      statusForm=StatusForm(request.POST,instance=hInstance.personStatus,prefix="statForm")
      if statusForm.is_valid():
        statusForm.save()
    if hForm.is_valid():
      hInstance=hForm.save()
    if sForm.is_valid():
      sForm.save()

    if sForm.is_valid() and hForm.is_valid():
      messages.info(request,'Person Updated')
      return redirect("/list/person")
  else:
    template = loader.get_template('people/editPerson.html')
    hForm = PersonForm(prefix="hForm",instance=hInstance)

    if hInstance==None:
      sForm= SocialForm(prefix="sForm")
      if moderatorCheck(request.user):
        statusForm=StatusForm(prefix="statForm")
    else:
      sForm= SocialForm(prefix="sForm",instance=hInstance.sID)
      if moderatorCheck(request.user):
        statusForm=StatusForm(instance=hInstance.personStatus,prefix="statForm")

    context={
      "personForm": hForm,
      "socialForm": sForm,
      "statusForm": statusForm
    }
    return HttpResponse(template.render(context, request))

@login_required  
def editProject(request,id=None):
  try:
    pInstance=get_object_or_404(Projects,pk=id)
  except:
    pInstance=None
  
  if request.method == 'POST':
    if pInstance==None:
      pInstance=Projects(projectName="Project Name")
      pInstance.sID=Socials()
      pInstance.projectStatus=Status()
      pInstance.projectStatus.save()
      pInstance.sID.save()
      pInstance.save()
    pForm = ProjectForm(request.POST,instance=pInstance,prefix="pForm")
    sForm= SocialForm(request.POST,request.FILES,instance=pInstance.sID,prefix="sForm")

    if moderatorCheck(request.user):
        statusForm=StatusForm(request.POST,prefix="statForm",instance=pInstance.projectStatus)
        if statusForm.is_valid():
          statusForm.save()
    if pForm.is_valid():
      pForm.save()
    if sForm.is_valid():
      sForm.save()
    if sForm.is_valid() and pForm.is_valid():
      messages.info(request,'Project Updated')
      return redirect("/list/project")
  else:
    template = loader.get_template('projects/editProject.html')
    pForm = ProjectForm(prefix="pForm",instance=pInstance)

    if pInstance==None:
      sForm= SocialForm(prefix="sForm")
      if moderatorCheck(request.user):
        statusForm=StatusForm(prefix="statForm")

    else:
      sForm= SocialForm(prefix="sForm",instance=pInstance.sID)
      if moderatorCheck(request.user):
        statusForm=StatusForm(prefix="statForm",instance=pInstance.projectStatus)

    context={
      "projectForm": pForm,
      "socialForm": sForm,
      "statusForm": statusForm
    }
    return HttpResponse(template.render(context, request))

@login_required
@user_passes_test(adminCheck)      
def delete(request,detailType,id):
  match detailType:
    case "person":
      try:
        instance=get_object_or_404(People,pk=id)
      except:
        messages.error(request,'Person Not Found')
        return redirect("/list/person")
      instance.delete()
      messages.info(request,'Person Deleted')
      return redirect("/list/person")
    case "project":
      try:
        instance=get_object_or_404(Projects,pk=id)
      except:
        messages.error(request,'Project Not Found')
        return redirect("/list/project") 
      instance.delete()
      messages.info(request,'Project Deleted')
      return redirect("/list/project")

@login_required
@user_passes_test(adminCheck)    
def approvals():
  #admin only page
  #approve, edit, delete submissions
  return