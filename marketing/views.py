from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, HelpDesk
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify



def blog_list(request):
    all_blogs  = Blog.objects.filter(published=True)
    freelancer_blogs = Blog.objects.filter(published=True, type=Blog.FREELANCER)
    client_blogs = Blog.objects.filter(published=True, type=Blog.CLIENT)

    context ={
        "all_blogs":all_blogs,
        "freelancer_blogs":freelancer_blogs,
        "client_blogs":client_blogs,
    }
    return render( request, "marketing/blog_list.html", context)


def blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug, published=True)

    context ={
        "blog":blog,
    }
    return render( request, "marketing/blog_detail.html", context)


@login_required
def support(request):
    for supports in HelpDesk.objects.filter(published=True):
        support = supports

    context ={
        "support":support,
    }
    return render( request, "marketing/support.html", context)


@login_required
def get_default_support(request, id):
    HelpDesk.objects.filter(pk=id, default=True).update(default=False)
    HelpDesk.objects.filter(pk=id).update(default=True)












































