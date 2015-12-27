from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from dss.models import application,incidence,UserProfile

def upload_application(instance, filename):
   # return "title_images/%s" % (filename)
    return '/'.join(['application_docs', str(instance.category), filename])

category =(
            ('Pests','Pests'),
            ('Disease','Disease'),
            ('Natural Disaster ','Natural Disaster'),
            ('Other','Other'),
    )
county = (
    ('Nyeri','Nyeri'),
    ('Kirinyaga','Kirinyaga'),
    ('Kiambu','Kiambu'),
    ('Laikipia','Laikipia'),

    )
incidence_status = (
        ('Average','Average'),
        ('Bad','Bad'),
        ('Very Bad','Very Bad'),
        ('Unknown','Unknown'),

    )

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('activation_key',)

class applicationForm(forms.ModelForm):
    class Meta:
        model = application
        exclude = ['user','app_id','date_applied','status']

class incidentForm(ModelForm):
    class Meta:
        model = incidence
        exclude = ['id']

class photoForm(ModelForm):
    class Meta:
        model = incidence
        exclude = ['photo']

class incidenceForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    telephone = forms.CharField(max_length=50, required=True)
    incidence_title = forms.CharField(max_length=50, required=True)
    category = forms.ChoiceField(choices=category) 
    county = forms.ChoiceField(choices=county)
    closest_town = forms.CharField(max_length=50,help_text= 'Mweiga')
    status = forms.ChoiceField(choices=incidence_status)
    #photo = forms.ImageField()
    #photo = forms.FileField(label='Upload photo', help_text='max. 42 megabytes')
    coordinates=forms.CharField(max_length=200, required=True)

    def clean(self):

        cleaned_data = self.cleaned_data

        first_name = cleaned_data.get("owner")
        last_name = cleaned_data.get("price")
        email = cleaned_data.get("email")
        telephone = cleaned_data.get("telephone")
        incidence_title = cleaned_data.get("incidence_title")
        category = cleaned_data.get("category")
        county = cleaned_data.get("county")
        closest_town = cleaned_data.get("closest_town")
        status = cleaned_data.get("status")
        coordinates = cleaned_data.get("coordinates")
    

        return cleaned_data

    
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
    #clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate email')

    #modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):        
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False # not active until he opens activation link
            user.save()

        return user

		