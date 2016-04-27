#import base64
#import hashlib


#def email_to_username(email):
#    return base64.urlsafe_b64encode(hashlib.sha256(email.lower()).digest())[:30]