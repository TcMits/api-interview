import datetime
from typing import Any
import jwt
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import User

User = get_user_model()


def login(instance: User, request: Any = None) -> User:
    # TODO: something
    def post(self,request):
        email = request.data[email]
        password = request.data[password]
        
        user = User.objects.filter(email=email, password=password).first()
        
        if user is None:
            print("User does not exist")
            
        if not user.check_password(password):
            print("Password is incorrect")
        
        payload = {
            'name': user.last_name + user.first_name,
            'email': user.email,
            'is_active': datetime.datetime.now()
        }
        
        token = jwt.encode(payload, algorithm="HS256").decode('utf8')
        
    
    instance.last_login = timezone.now()
    instance.save(update_fields=["last_login"])
    return instance
