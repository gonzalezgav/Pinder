from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="Ingrese su nombre")
    last_name = forms.CharField(max_length=100, label="Ingrese su apellido")
    username = forms.CharField(max_length=50, label="Ingrese su nombre de usuario")
    email = forms.EmailField(label="Ingrese su email",widget=forms.EmailInput)
    password1: forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2: forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
        help_texts={k:"" for k in fields}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['nombre','especie','image','sexo','edad','tamanio','vacunas_aplicadas','castracion','desparasitado','discapacidad','content']
  
           
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="Ingrese su nombre")
    last_name = forms.CharField(max_length=100, label="Ingrese su apellido")
    username = forms.CharField(max_length=50, label="Ingrese su nombre de usuario")
    email = forms.EmailField(label="Ingrese su email",widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',]


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="Ingrese su nombre")
    last_name = forms.CharField(max_length=100, label="Ingrese su apellido")
    username = forms.CharField(max_length=50, label="Ingrese su nombre de usuario")
    email = forms.EmailField(label="Ingrese su email",widget=forms.EmailInput)
    class Meta:
        model = Profile
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'image',
                  'dni',
                  'sexo',
                  'edad',
                  'telefono',
                  'localidad',
                  'provincia' ,
                  'ocupacion',
                  'carga_horaria',
                  'dias_homeoffice',
                  'cantidad_hijos',
                  'cantidad_mascotas',
                  'especie_mascota',
                  'espacio_abierto',
                  'ig',
                  'fb',
                  'tw',)


class PostCommentForm(forms.ModelForm):    
    comment = forms.CharField(
            widget=forms.Textarea(attrs={
            'placeholder': 'Agregar Comentario'
            }),
        required=True
        )

    class Meta:
        model=PostComment
        fields=['comment']              