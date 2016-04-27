from django import forms
from django.utils.translation import ugettext_lazy as _
from regform.models import UserTable
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.password_validation import *

#from nocaptcha_recaptcha.fields import NoReCaptchaField


class RegistrationForm(forms.Form):
    COUNTRY_CHOICES = (('am', 'America'), ('eu', 'Europe'), ('as', 'Asia'), ('af', 'Africa'),
                         ('au', 'Australia'), ('oc', 'Oceania'), ('an', 'Antartica'),)
    ETHNICITY_CHOICES = (('ame', 'American'), ('eup', 'Europeon'), ('afr', 'African'),
                         ('aus', 'Australian'),)
    LANGUAGES_KNOWN_BY = (('en', 'English'), ('hi', 'Hindi'), ('ch', 'China'),)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
    
    first_name = forms.RegexField(regex=r"^[a-zA-Z{0-9}']+$", widget=forms.TextInput(attrs=dict(required=True, max_length=50)), min_length=0,
                                  label=_("First Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    middle_name = forms.RegexField(regex=r"^[a-zA-Z{0-9}']+$", widget=forms.TextInput, required=False, max_length=50,
                                  label=_("Middle Name"),
                                  error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    last_name = forms.RegexField(regex=r"^[a-zA-Z{0-9}']+$", widget=forms.TextInput, required=False,max_length=50, 
                                  label=_("Last Name"), 
                                  error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=50)), label=_("Email address"))
    mobile_no = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False,
                                    error_messages={ 'invalid': _("Phone number must be entered in the format: '+919999999'. Up to 15 digits allowed.") })
    alternate_mobile_no = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False,
                                    error_messages={ 'invalid': _("Phone number must be entered in the format: '+919999999'. Up to 15 digits allowed.") })
    #birthdate = forms.DateField(widget = SelectDateWidget(required = False, years = range(2022, 1930, -1))) # make birthdate drop down selectable
    date_of_birth = forms.DateField(label='Date of birth', widget=forms.DateInput(attrs={'validate-date': '^(\d{4})-(\d{1,2})-(\d{1,2})$'}),
                                        help_text='Allowed date format: yyyy-mm-dd')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Gender',
                                    error_messages={'invalid_choice': 'Please select your gender'})
    ethnicity = forms.ChoiceField(choices=ETHNICITY_CHOICES, label='Ethnicity',
                                    error_messages={'invalid_choice': 'Please select your ethnicity'})
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, label='Country',
                                    error_messages={'invalid_choice': 'Please select your country'})
    languages_known = forms.ChoiceField(choices=LANGUAGES_KNOWN_BY, label='language',
                                    error_messages={'invalid_choice': 'Please select your language'})
    password1 = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs=dict(required=True,
                                                                      max_length=50,
                                                                      render_value=False)),
                                label=_("Password"))
    password2 = forms.CharField(min_length=6,widget=forms.PasswordInput(attrs=dict(required=True,
                                                                      max_length=15,
                                                                      render_value=False)),
                                label=_("Password (again)"))


    #captcha = NoReCaptchaField()
    
    def __init__(self, *args, **kw):
        self.user_obj = kw.pop('user', None)
        super(RegistrationForm, self).__init__(*args, **kw)
        if self.user_obj and not self.user_obj.is_anonymous():
            del self.fields['password1']
            del self.fields['password2']
            del self.fields['email']
            #del self.fields['captcha']
            try:
                self.fields["first_name"].initial = self.user_obj.usertable.first_name
                self.fields["middle_name"].initial = self.user_obj.usertable.middle_name
                self.fields["last_name"].initial = self.user_obj.usertable.last_name
                self.fields["mobile_no"].initial = self.user_obj.usertable.mobile_no
                self.fields["alternate_mobile_no"].initial = self.user_obj.usertable.alternate_mobile_no
                self.fields["date_of_birth"].initial = self.user_obj.usertable.date_of_birth
                self.fields["gender"].initial = self.user_obj.usertable.gender
                self.fields["ethnicity"].initial = self.user_obj.usertable.ethnicity
                self.fields["country"].initial = self.user_obj.usertable.country
                self.fields["languages_known"].initial = self.user_obj.usertable.languages_known
               
            except UserTable.DoesNotExist:
                pass
 
    def clean_email(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("The email already exists. Please try another one."))
 
    def clean_password1(self):
        if 'password1' in self.cleaned_data and len(self.cleaned_data['password1']) < 6:
            raise forms.ValidationError(_("The Password must be more than 6 chars."))
        return self.cleaned_data['password1']
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class LoginForm(forms.Form):
    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

   

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=50)), label=_("Email address"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True,
                                                                    max_length=50,
                                                                    render_value=False)),
                                label=_("Password"))
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    
                )

        if user:
            self.user_cache = authenticate(username=user.username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    
                )
            else:
                #self.confirm_login_allowed(self.user_cache)
                pass

        return self.cleaned_data
        
    def get_user(self):
        return self.user_cache
