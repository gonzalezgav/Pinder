from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.urls import  reverse_lazy
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView,DeleteView
from django.db.models import Q

# Create your views here.


def landing(request):
    return render(request, "pinderApp/index.html")

def about(request):
    return render(request, "pinderApp/about.html")


@login_required
def searchbox(request):
    search = request.GET['search']
    usersearch = User.objects.filter(username__icontains=search)
    if usersearch:
         context={
             'search':search,
             'usersearch':usersearch,
         }
         messages.success(request, 'Resultados encontrados con exito')
         return  render(request,"pinderApp/search.html",context)
    else:
     messages.error(request, 'No se encontro')
     return redirect('feed')

    


@login_required
def feed(request):

  data = Post.objects.all()
  context = {'data': data}
  return render(request, "pinderApp/feed.html", context)

@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = current_user
            post.save()
            messages.success(request, 'Post creado con exito.')
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, "pinderApp/post.html", {'form': form})

@login_required
def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
     user = User.objects.get(username=username)
     posteos = user.posteos.all()
    else:
     posteos = current_user.posteos.all()
     user = current_user

    context= {
        'user':user,
        'posteos':posteos,
        }        
              
    return render(request, 'pinderApp/profile.html', context)

@login_required
def follow(request,username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'Siguiendo a {username}')
    return redirect('profile', username=to_user)

@login_required
def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
	rel.delete()
	messages.success(request, f'Ya no sigues a {username}')
	return redirect('profile', username=to_user)

@login_required
def followersList(request, username):
    user = User.objects.get(username=username)
    follows = user.followers.all()
    context= {
        'user':user,
        'follows':follows
        }      
    return render(request, 'pinderApp/followers_list.html', context)

@login_required
def editProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    user__basic__info = User.objects.get(id=user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES , instance=profile)
        if form.is_valid():
          user__basic__info.first_name= form.cleaned_data.get('first_name')
          user__basic__info.last_name= form.cleaned_data.get('last_name') 
          user__basic__info.username= form.cleaned_data.get('username') 
          user__basic__info.email= form.cleaned_data.get('email') 
          
          profile.image = form.cleaned_data.get('image')
          profile.dni = form.cleaned_data.get('dni')
          profile.sexo = form.cleaned_data.get('sexo')
          profile.edad = form.cleaned_data.get('edad')
          profile.telefono = form.cleaned_data.get('telefono')
          profile.localidad = form.cleaned_data.get('localidad')
          profile.provincia = form.cleaned_data.get('provincia')
          profile.ocupacion = form.cleaned_data.get('ocupacion')
          profile.carga_horaria = form.cleaned_data.get('carga_horaria')
          profile.dias_homeoffice = form.cleaned_data.get('dias_homeoffice')
          profile.cantidad_hijos = form.cleaned_data.get('cantidad_hijos')
          profile.espacio_abierto = form.cleaned_data.get('espacio_abierto')
          profile.ig = form.cleaned_data.get('ig')
          profile.fb = form.cleaned_data.get('fb')
          profile.tw = form.cleaned_data.get('tw')


          profile.save()
          user__basic__info.save()
          messages.success(request, f'Perfil actualizado con exito.')
          return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile)
    
    context={
      'form':form,
    } 
    return render(request, "pinderApp/profile_form.html", context)

@login_required
def gatos(request):
    cat = Post.objects.filter(especie='2')
    context = {'cat':cat}
    return render(request, 'pinderApp/gatos.html',context)

@login_required
def perros(request):
    dog = Post.objects.filter(especie='1')
    context = { 'dog':dog}
    return render(request, 'pinderApp/perros.html',context)    

def register(request):
    if request.user.is_authenticated:
        return redirect('feed')
    else:
        if request.method == 'POST':
         form = UserRegisterForm(request.POST)
         if form.is_valid():
             form.save()
             user = form.cleaned_data.get('username')
             password = form.cleaned_data.get('password1')
             username = authenticate(username=user, password=password)
             login(request, username)
             messages.success( request, f'Hola {user}, tu usuario se creo con exito.')
             return redirect('feed')
        else:
          form = UserRegisterForm()
          context = {'form': form}
          return render(request, "pinderApp/register.html", context)    

class PostDetailView(View,LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostCommentForm()

        comments = PostComment.objects.filter(post=post).order_by('-timestamp')

        context = {
            'post': post,
            'form': form,
            'comments':comments
        }
 
        return render(request,'pinderApp/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = PostComment.objects.filter(post=post).order_by('-timestamp')
    
        context ={
           'post':post,
           'form':form,
           'comments':comments,
        }   
        return render(request,'pinderApp/post_detail.html',context)
    
class PostEditView(UpdateView ,LoginRequiredMixin,UserPassesTestMixin):
    model=Post
    fields='__all__'
    template_name= 'pinderApp/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk':pk})

    def test_func(self):
        post = self.ger_object()
        return self.request.user == post.author  

class PostDeleteView(DeleteView ,LoginRequiredMixin,UserPassesTestMixin):
    model=Post
    fields='__all__'
    template_name= 'pinderApp/post_delete.html'
    success_url = reverse_lazy('feed')

    def test_func(self):
        post = self.ger_object()
        return self.request.user == post.author  

class AddLike(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)    

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)    

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=PostComment
    template_name="pinderApp/comment_delete.html"

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentEditView(UpdateView ,LoginRequiredMixin,UserPassesTestMixin):
    model = PostComment
    fields = ['comment']
    template_name = 'pinderApp/comment_edit.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={'pk':pk})        
