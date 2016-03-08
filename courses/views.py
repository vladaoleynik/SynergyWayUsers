from django.shortcuts import render
from django.views import generic


class CourseView(generic.TemplateView):
    template_name = 'courses/courses.html'
