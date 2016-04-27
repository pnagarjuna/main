from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


#gender_list = (('M', 'Male'), ('F', 'Female' ))

# Create your models here.
class UserTable(models.Model):
    ame = 'AM'
    eup = 'EUP'
    afr ='AFR'
    aus ='AUS'
    M = 'm'
    am ='AM'
    eu = 'EU'
    asi = 'AS'
    af = 'AF'
    au = 'AU'
    oc = 'OC'
    an = 'AN'
    en = 'EN'
    hi = "HI"
    ch = 'CH'
    ETHNICITY_CHOICES = (('ame', 'American'), ('eup', 'Europeon'), ('afr', 'African'),
                         ('aus', 'Australian'),)
    COUNTRY_CHOICES = (('am', 'America'), ('eu', 'Europe'), ('asi', 'Asia'), ('af', 'Africa'),
                         ('au', 'Australia'), ('oc', 'Oceania'), ('an', 'Antartica'),)
    LANGUAGES_KNOWN_BY = (('en', 'English'), ('hi', 'Hindi'), ('ch', 'China'),)
    GENDER_CHOICES = ( 
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, max_length=100)
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format")
    mobile_no = models.CharField(max_length=15)
    #mobile_no = models.CharField(max_length=15, validators=[phone_regex], blank=False)            
    alternate_mobile_no = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank = True) # True makes this field optional                                                        
    gender = models.CharField(max_length = 50, choices=GENDER_CHOICES, default=M, blank = False)
    ethnicity  = models.CharField(max_length=5, choices = ETHNICITY_CHOICES, default=ame, blank = False)
    country = models.CharField(max_length=10, choices = COUNTRY_CHOICES, default=am, blank = False)
    languages_known = models.CharField(max_length=7, choices = LANGUAGES_KNOWN_BY, default=en, blank = False)
    error = models.CharField(max_length=200)
   
    def __str__(self):
       return "%s-%s" %(self.first_name, self.last_name)
