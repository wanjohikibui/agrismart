__author__ = 'alphabuddha'

from dss.forms import *
from dss.models import *
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
from icalendar import Calendar, Event
from django.db.models import get_model
from django.contrib.sites.models import Site

def contact_us(request):
    return render_to_response("/temp/contact-us.html", locals(), context_instance=RequestContext(request))

def form_error(request):
    return render_to_response('temp/error.html')

def form_success(request):
    return render_to_response('temp/success.html')

def register_success(request):
    return render(request, 'registration/registration_complete.html')

def about(request):
    return render_to_response("temp/about-us.html", locals(), context_instance=RequestContext(request))

def calendar(request):
    return render_to_response("temp/calendar.html", locals(), context_instance=RequestContext(request))

def export(request, event_id):
    event = get_model('events', 'event').objects.get(id = event_id)

    cal = Calendar()
    site = Site.objects.get_current()

    cal.add('prodid', '-//%s Events Calendar//%s//' % (site.name, site.domain))
    cal.add('version', '2.0')

    site_token = site.domain.split('.')
    site_token.reverse()
    site_token = '.'.join(site_token)

    ical_event = Event()
    ical_event.add('summary', event.description)
    ical_event.add('dtstart', event.start)
    ical_event.add('dtend', event.end and event.end or event.start)
    ical_event.add('dtstamp', event.end and event.end or event.start)
    ical_event['uid'] = '%d.event.events.%s' % (event.id, site_token)
    cal.add_component(ical_event)

    response = HttpResponse(cal.as_string(), mimetype="text/calendar")
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % event.slug
    return response

class BlogIndex(generic.ListView):
    queryset = Entry.objects.published()
    template_name = "temp/feeds.html"
    paginate_by = 2

class BlogDetail(generic.DetailView):
    model = Entry
    template_name = "temp/post.html"

@login_required
def status(request):
    user = request.user.get_full_name()
    applications = application.objects.filter(user=request.user)
    return render_to_response("temp/status.html", {"applications": applications}, context_instance=RequestContext(request))

def map(request):
    return render_to_response("temp/portal.html", locals(), context_instance=RequestContext(request))

def points(request):
    return render_to_response("temp/points.html", locals(), context_instance=RequestContext(request))

def incident_portal(request):
    form = incidentForm
    if request.method == 'POST':
        form = incidentForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            #return index(request)
            return HttpResponseRedirect(reverse("incident"))
        else:
            print form.errors
    else:
        form = incidentForm()
    return render(request, 'temp/incident.html', {'form': form})

def weather_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': MonthlyWeatherByCity.objects.all()},
              'terms': [
                'number',
                'males',
                'females']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'number': [
                    'females',
                    'males']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response({'weatherchart': cht})

@login_required
def application_portal(request):
    form = applicationForm
    if request.method == 'POST':
        form = applicationForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            cd = form.cleaned_data

            email_to = cd['email']
            subject = "{0} Update".format(cd['first_name'])
            message = "Applicant: {0}\n\n Your application has been received".format(
                cd['last_name'])
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email_to,])
            new_form.save()
            messages.success(request, 'Application Sent successfully')
            return HttpResponseRedirect(reverse("apply"))
        else:
            print form.errors
    else:
        form = applicationForm()
    images=application.objects.all()
    return render(request, 'temp/apply.html', {'form': form,'images':images})



def add_point(request):

    if request.method == 'POST':
        form = incidenceForm(request.POST)
        if form.is_valid():
            new_point = incidence()
            cd = form.cleaned_data
            new_point.first_name = cd['first_name']
            new_point.last_name = cd['last_name']
            new_point.email = cd['email']
            new_point.telephone = cd['telephone']
            new_point.incidence_title = cd['incidence_title']
            new_point.category = cd['category']
            new_point.county = cd['county']
            new_point.closest_town = cd['closest_town']
            new_point.status = cd['status']
            #new_point.photo = cd['photo']
            coordinates = cd['coordinates'].split(',')
            new_point.geom = Point(float(coordinates[0]), float(coordinates[1]))
            
            new_point.save()

            email_to = cd['email']
            subject = "{0} Update".format(cd['incidence_title'])
            message = "Applicant: {0}\n\n Your incidence has been received.Thank you for the report".format(
                cd['first_name'])
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,[email_to,])
            
            return HttpResponseRedirect('/incidences/')


        else:
            return HttpResponseRedirect('/incidences/')

    else:
        form = incidenceForm()

    args = {}
    args.update(csrf(request))
    args['form'] = incidenceForm()
    return render_to_response('temp/incidence.html', args)


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid(): 
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile                                                                                                                                  
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within 48hours http://localhost:8000/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',[email], fail_silently=False)
            messages.success(request, 'Account created successfully.Check your mail to activate!')
            return HttpResponseRedirect('/register/')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('temp/register.html', args, context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        HttpResponseRedirect('')

    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if user_profile.key_expires < timezone.now():
        return render_to_response('temp/confirm_expired.html')
    
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('temp/confirm.html')
    messages.success(request, 'Confirmation successfull')

def user_login(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            
            if user.is_active:

                if user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect('/admin/')
                else:

                    login(request, user)
                    return HttpResponseRedirect('/')
                
            else:
                #return HttpResponseRedirect(reverse("login"))
                messages.error(request, "Error")
        else:
            
            messages.error(request, "Invalid username and password.Try again!")
            return render_to_response('temp/login.html', args, context_instance=RequestContext(request))

    
    else:
        
        return render(request, 'temp/login.html', {})

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('accounts/login/')

def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response
    messages.success(request, 'Password changed successfully!')

def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'noreply@ke_ladm.com'),
                ['swanjohi9@gmail.com'], #email address where message is sent.
            )
            messages.success(request, 'Your message has been sent.Thank you for contacting us!') 
            
            return HttpResponseRedirect('/contacts/')
    return render(request, 'temp/contact-us.html',
        {'errors': errors}) 

def thanks(request):
    return render_to_response('temp/thanks.html')
