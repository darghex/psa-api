from django.shortcuts import render
import requests
from django.http import HttpResponse
from bs4 import BeautifulSoup
import json
from django.views.decorators.csrf import csrf_exempt
from psa.psa_backend import PSABackend

def clean_text(__str):
    
    return __str.replace(u'\u00a0'," ").replace(u'\xa0'," ")

@csrf_exempt
def login(request):
    if not request.method == 'POST':
        return HttpResponse( "Invalid Method. Send Request with Post Method!", content_type='application/json' , status = 405)
    else:
        auth = PSABackend()
        user = auth.authenticate(request.POST['user'], request.POST['password'])      
        if user:
            output = json.dumps( {"id": user.id, "name": user.name, "document": user.id, "email": user.email })        
        return HttpResponse( output, content_type='application/json' , status = 200)
    except:
        return HttpResponse( "Login Failed", content_type='text/html' , status = 401)