from django.shortcuts import render
from django.views import generic


class UsersView(generic.TemplateView):
    template_name = 'users/user-list.html'
