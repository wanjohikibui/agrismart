__author__ = 'alphabuddha'

from dss.forms import *
from cropper.models import *
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.gis.geos import Point
from vectorformats.Formats import Django, GeoJSON
from django.core.context_processors import csrf
import uuid
from django.db.models import Q
from django.views import generic
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import timezone
import hashlib, datetime, random
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.core import serializers
from chartit import DataPool, Chart
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth import logout
from django.contrib.auth import views
from django.core.paginator import Paginator, InvalidPage, EmptyPage
# Create your views here.

def planner(request):
    return render_to_response("temp/planner.html", locals(), context_instance=RequestContext(request))

def analyzer(request):
    return render_to_response("temp/analyzer.html", locals(), context_instance=RequestContext(request))

class cropIndex(generic.ListView):
	queryset = cropping.objects.approved()
	#properties = crop.objects.all()
	template_name = "temp/crop.html"
	paginate_by = 10
	
	def get(self, request, *args, **kwargs):
		crops_list = cropping.objects.all()
		var_get_search = request.GET.get('search_box')
		if var_get_search is not None:
			crops_list = crops_list.filter(Q(name__icontains=var_get_search)| Q(category__icontains = var_get_search)| Q(soil__icontains = var_get_search))
		paginator = Paginator(crops_list, 10) # Show 25 contacts per page

		# Make sure page request is an int. If not, deliver first page.
		try:
			page = int(request.GET.get('page', '1'))
		except ValueError:
			page = 1

		# If page request (9999) is out of range, deliver last page of results.
		try:
			crops = paginator.page(page)
		except (EmptyPage, InvalidPage):
			crops = paginator.page(paginator.num_pages)
		return render(request, self.template_name, {'crops': crops,'crops_list':crops_list})

class cropDetail(generic.DetailView):	
	model = cropping
	template_name = "temp/crops.html"
