from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from django.contrib.auth.decorators import login_required
from .forms import ProjectCreationForm, ProjectmodifyForm, ProjectReopenForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from client.models import Client
from account.permission import user_is_freelancer, user_is_client
from account.models import Customer
from teams.models import Team
from applications.models import Application
from django.http import JsonResponse
from teams.controller import monthly_projects_applicable_per_team
from django.conf import settings
from django.contrib import messages
import requests
import base64
import json
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime, timezone, timedelta
from teams.controller import monthly_projects_applicable_per_team
from notification.utilities import create_notification


@login_required
@user_is_client
def create_project(request):
    if request.method == 'POST':
        projectform = ProjectCreationForm(request.POST, request.FILES)

        if projectform.is_valid():
            project = projectform.save(commit=False)
            project.created_by = request.user
            project.slug = slugify(project.title)
            project.save()
            projectform.save_m2m()  # for saving many-to-many items in forms

            messages.info(request, 'Project received. Hold on as we review')

            return redirect('account:dashboard')
    else:
        projectform = ProjectCreationForm()

    context = {
        'projectform': projectform,
    }
    return render(request, 'projects/post_project.html', context)


def project_single(request, project_slug):
    # if request.user.user_type == Customer.CLIENT:
    project = get_object_or_404(Project, slug=project_slug)
    profile_view = get_object_or_404(Client, user=project.created_by, user__is_active=True)
    applications = Application.objects.filter(project = project)
    application_limit = monthly_projects_applicable_per_team(request)

    context = {
        "projectdetail": project,
        'project':project,  
        'profile_view':profile_view,  
        'application_limit':application_limit,  
        'applications':applications,  
        # 'monthly_projects_applicable_per_team':monthly_projects_applicable_per_team(request),  
  
    }
    return render(request, 'projects/project_detail.html', context)


@login_required
@user_is_client
def update_project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, created_by=request.user)

    if request.method == 'POST':
        projectform = ProjectmodifyForm(request.POST, request.FILES, instance=project)

        if projectform.is_valid():
            projectform.save()

            messages.success(request, 'The Changes were saved successfully!')

            return redirect('account:dashboard')

    else:
        projectform = ProjectmodifyForm(instance=project)
    context = {
        "projectform": projectform,
        "project": project,
    }
    return render(request, 'projects/update_project.html', context)


@login_required
@user_is_client
def reopen_project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, created_by=request.user)

    if request.method == 'POST':
        projectform = ProjectReopenForm(request.POST, instance=project)

        if projectform.is_valid():
            projectform.save()

            messages.success(request, 'The project was extended successfully!')

            return redirect('account:dashboard')

    else:
        projectform = ProjectReopenForm(instance=project)
    context = {
        "projectform": projectform,
        "project": project,
    }
    return render(request, 'projects/reopen_project.html', context)


@login_required
@user_is_client
def active_project(request):
    active_projects = Project.objects.filter(created_by=request.user, status=Project.ACTIVE)
    context = {
        'active_projects': active_projects,
    }
    return render(request, 'projects/active_project.html', context)


@login_required
@user_is_client
def review_project(request):
    review_projects = Project.objects.filter(created_by=request.user, status=Project.REVIEW)

    context = {
        'review_projects':review_projects,
    }
    return render(request, 'projects/review_project.html', context)


@login_required
@user_is_client
def archived_project_view(request):
    archived_projects = Project.objects.filter(created_by=request.user, status=Project.ARCHIVED)

    context = {
        'archived_projects':archived_projects,
    }
    return render(request, 'projects/archived_project.html', context)


@login_required
@user_is_client
def archive_project(request, project_slug):
    Project.objects.filter(created_by=request.user, status=Project.ACTIVE, slug=project_slug).update(status = Project.ARCHIVED)

    messages.success(request, 'The project was archived successfully!')

    return redirect('projects:active_project')


@login_required
@user_is_client
def restore_archive_project(request, project_slug):
    Project.objects.filter(created_by=request.user, status=Project.ARCHIVED, slug=project_slug).update(status = Project.ACTIVE)

    messages.success(request, 'The project was restored successfully!')

    return redirect('projects:archived_project_view')


# This will appear in search even without login
def project_list(request):
    project = Project.objects.filter(status=Project.ACTIVE)
    # paginator for the projects page
    paginator = Paginator(project, 7)
    page_var = "page"
    page = request.GET.get(page_var)
    try:
        paginated_project = paginator.page(page)
    except PageNotAnInteger:
        paginated_project = paginator.page(1)
    except EmptyPage:
        paginated_project = paginator.page(paginator.num_pages)

    context = {
        "listing": paginated_project,
        "page_var": page_var
    }
    return render(request, 'projects/project_listing.html', context)


@login_required
@user_is_client
def delete_project(request, pk=None):
    project_delete = Project.objects.get(pk=pk, created_by=request.user)
    project_delete.delete()
    return redirect('projects:my_projects')
