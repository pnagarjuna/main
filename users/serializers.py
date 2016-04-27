from rest_framework import serializers, exceptions

from django.contrib.auth.models import User
from rest_framework.response import Response

from regform.models import UserTable
from django.http import HttpResponse
from django.http import Http404

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status


ETHNICITY_CHOICES = (('ame', 'American'), ('eup', 'Europeon'), ('afr', 'African'),
                         ('aus', 'Australian'),)
COUNTRY_CHOICES = (('am', 'America'), ('eu', 'Europe'), ('asi', 'Asia'), ('af', 'Africa'),
                         ('au', 'Australia'), ('oc', 'Oceania'), ('an', 'Antartica'),)
LANGUAGES_KNOWN_BY = (('en', 'English'), ('hi', 'Hindi'), ('ch', 'China'),)
GENDER_CHOICES = ( 
        ('M', 'Male'),
        ('F', 'Female'),
    )

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        #content = JSONRenderer().render(data)
        content = JSONRenderer().render(data, renderer_context={'indent':4})
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

#from regform.utils import email_to_username
class UserTableSerializer(serializers.Serializer):
    #errors ={}
    #import pdb; pdb.set_trace()
    pk = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    password = serializers.CharField(required=False, allow_blank=False, max_length=15)
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=50)
    middle_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=True, allow_blank=True, max_length=50)
    email = serializers.EmailField(required=True, allow_blank=False, max_length=50)
    mobile_no = serializers.CharField(required=False, max_length=15, min_length=9, error_messages={'invalid': ("Phone number must be entered in the format: '+919999999'. Up to 15 digits allowed.")})
    alternate_mobile_no = serializers.CharField(required=False, allow_blank=True, max_length=15)
    date_of_birth = serializers.CharField(required=True, allow_blank=False)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True, allow_blank=False)
    ethnicity = serializers.ChoiceField(required=False, choices = ETHNICITY_CHOICES, allow_blank=True)
    country = serializers.ChoiceField(required=False, choices = COUNTRY_CHOICES, allow_blank=True)
    languages_known = serializers.ChoiceField(required=False, choices = LANGUAGES_KNOWN_BY, allow_blank=True)
    
    def create(self, validated_data):
        #user_name = validated_data['user_name']
        #import pdb; pdb.set_trace()
        user_name = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        middle_name = validated_data.get('middle_name', '')
        last_name = validated_data['last_name']
        mobile_no = validated_data.get('mobile_no', '')
        alternate_mobile_no = validated_data.get('alternate_mobile_no', '')
        date_of_birth = validated_data['date_of_birth']
        gender = validated_data['gender']
        ethnicity = validated_data.get ('ethnicity', '')
        country = validated_data.get('country', '')
        languages_known = validated_data.get('languages_known', '')
        email = validated_data['email']
        
        try:
            user = User.objects.get(username=user_name)
            raise serializers.ValidationError('this email is already registered')
            #return JSONResponse({'errors':'User already exists'}, 
               # status=status.HTTP_404_NOT_FOUND)
        except serializers.ValidationError: 
           
            return  JSONResponse({'errors':'112User already exists'},
                status=status.HTTP_404_NOT_FOUND )

            raise Http404("dghksgjsg")

        except User.DoesNotExist: 
            #user = User.objects.create(email=email,
            #                  username=email_to_username(email))    
            user = User.objects.create(email = email)
            user.set_password(password)
            user.save()
            return UserTable.objects.create(user=user, first_name=first_name, middle_name=middle_name,last_name=last_name,  
                                           email=email, mobile_no=mobile_no, alternate_mobile_no=alternate_mobile_no, 
                                          date_of_birth=date_of_birth, gender=gender, ethnicity=ethnicity, country=country, 
                                          languages_known=languages_known)


    def update(self, instance, validated_data):
        #import pdb; pdb.set_trace()
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile_no = validated_data.get('mobile_no', instance.mobile_no)
        instance.alternate_mobile_no = validated_data.get('alternate_mobile_no', instance.alternate_mobile_no)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.ethnicity = validated_data.get ('ethnicity', instance.ethnicity)
        instance.country = validated_data.get('country', instance.country)
        instance.languages_known = validated_data.get('languages_known', instance.languages_known)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance