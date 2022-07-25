from email.mime import image
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# MODELO DE PERFIL DEL USUARIO
SEXO_USUARIO = (
    ("1", "Masculino"),
    ("2", "Femenino"),
    ("3", "Prefiero no decirlo")
)

ESPACIO_USUARIO = (
    ("1", "Patio o Parque"),
    ("2", "Terraza o Balcon"),
    ("3", "No poseo"),
)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics',
                              default='../media/user.png')
    dni = models.PositiveIntegerField(null=True)
    sexo = models.CharField(
        max_length=30,
        choices=SEXO_USUARIO
    )
    edad = models.PositiveIntegerField(null=True)
    telefono = models.PositiveIntegerField(null=True)
    localidad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=30)
    ocupacion = models.CharField(max_length=50)
    carga_horaria = models.PositiveIntegerField(null=True)
    dias_homeoffice = models.PositiveIntegerField(null=True)
    cantidad_hijos = models.PositiveIntegerField(null=True)
    cantidad_mascotas = models.PositiveIntegerField(null=True)
    especie_mascota = models.CharField(max_length=50)
    espacio_abierto = models.CharField(
        max_length=40,
        choices=ESPACIO_USUARIO
    )
    ig = models.URLField(null=True)
    fb = models.URLField(null=True)
    tw = models.URLField(null=True)

    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user)\
            .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user)\
        .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def __str__(self):
	    return f'Perfil de {self.user.username}'



# POSTEO DE ANIMAL
ESPECIE_OPCIONES = (
    ("1", "Perro"),
    ("2", "Gato"),
)

SEXO_OPCIONES = (
    ("1", "Macho"),
    ("2", "Hembra"),
)

TAMANIO_OPCIONES = (
("1", "Grande"),
("2", "Mediano"),
("3", "Chico"),
)

CASTRACION_OPCIONES = (
    ("1", "Si"),
    ("2", "No"),
)

DESPARASITADO_OPCIONES = (
    ("1", "Si"),
    ("2", "No"),
)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posteos') 
    likes = models.ManyToManyField(User,blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User,blank=True, related_name='dislikes')
    timestamp = models.DateTimeField(default=timezone.now)
    nombre = models.CharField(max_length=30, blank=True,null=True)
    especie = models.CharField(
        max_length=20,
        choices=ESPECIE_OPCIONES,
        default="Elegir Opcion"

          )
    sexo = models.CharField(
        max_length=20,
        choices=SEXO_OPCIONES, 
        default="Elegir Opcion"

    )
    edad = models.PositiveIntegerField(blank=True,null=True)
    tamanio = models.CharField(
        max_length=20,
        choices=TAMANIO_OPCIONES,
        default="Elegir Opcion"

    )
    vacunas_aplicadas = models.PositiveIntegerField(blank=True,null=True)
    castracion = models.CharField(
        max_length=20,
        choices=CASTRACION_OPCIONES, 
        default="Elegir Opcion"

    )
    desparasitado = models.CharField(
        max_length=20,
        choices=DESPARASITADO_OPCIONES,
        default="Elegir Opcion"
    )
    discapacidad = models.CharField(max_length=150, blank=True)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='posteos', null=True)    

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username}: {self.content}'


class PostComment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_posteos') 
    timestamp = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  blank=True, null=True,)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return Post.objects.filter(parent=self).order_by('-timestamp').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


    
class Relationship(models.Model):
	from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} to {self.to_user}'

	class Meta:
		indexes = [
		models.Index(fields=['from_user', 'to_user',]),
		]