from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.hashers import make_password

def clean_text(__str):
    
    return __str.replace(u'\u00a0'," ").replace(u'\xa0'," ")

class PSABackend(object):
    """
    Backend de autenticacion para cambiar el comportamiento de logueo de usuarios locales y cargar los de la universidad
    """
    def authenticate(self, username=None, password=None):
        
        try:
            ## Detectamos si ya existen guardados previamiente en nuestra DB locals
            # FixMe: Verificar cuando usuario cambie contrasena
            user = User.objects.get(username=username)
            pass_valid = check_password(password, user.password) 
            
            if pass_valid:
                return user
        except User.DoesNotExist:
            # SI el usuario no existe verificamos que sea un usuario de la plataforma academica PSA
            url_login = "http://toro.unipiloto.edu.co:7777/pls/orasso/orasso.wwsso_app_admin.ls_login"
            token ="""v1.2~CCAB46A6~303240BBCD9C52E42DD9298DDF5F9F9748AD0E7F4BC88D2589B5763A5CC95ED6638C0034A88C5C7EE01CA736068AAEC20AA5C64EEC3A20081073BEA448ACB7A7DFB21DB8DE343D843B8E011FE0C89B51478F21A1DBADCF0FA9FAD79F8D310BDCB919B4DD7ABE847E7F4FAB5A89A18AA91E3FBA558B382765314AC154563D0C8569418EB7119B0F137DA325B7F76B27E1A46B71BF3D76E502A8C5D27CD19F30E22A7FF6D0E622547DC193582216C24E83FF367589838D5F75915FC08A4EE0FA70AC781E341F606C99F84E81799378F1BC19FD7CC38A521336833B5A4E7B2738489CC3C1305C4A4C1AF07B5A4988A6542DB35807DE07E9B18C876FD34D43A8C90817B87EFD905A97F2"""
            credenciales = { 'ssousername': username, 'p_request': '', 'login': 'Login', 'site2pstoretoken': token, 'password': password,  }
            request_session = requests.session()
            request = request_session.post(url_login, credenciales)
            try:
                request = request_session.get("http://aguila.unipiloto.edu.co:7777/portal/page/portal/uxxiportal/academico/datos")
                bs = BeautifulSoup(request.text, "html5lib")
                nombre = clean_text(bs.findAll("span", {"class": "PortletHeading2"})[1].get_text())
                data = bs.findAll("span", {"class": "PortletText1"})
                documento = clean_text( data[0].get_text()).strip()
                user = User()
                user.first_name = nombre
                user.username = username
                user.email = "%s@upc.edu.co" % username
                user.is_staff = True
                user.is_active = True
                user.is_superuser = True
                user.password = make_password(password)
                user.save()
                return user
            except:
                pass  


    def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None 