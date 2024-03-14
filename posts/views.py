from django.shortcuts import render, redirect ,get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import (
    CreateView ,ListView,DetailView,UpdateView,DeleteView,RedirectView,View)
from django.urls import reverse
from .models import User
from .forms import ProfileForm ,UserCreationForm
from allauth.account.views import PasswordChangeView
from django.contrib.auth.views import LoginView
from .forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email') 
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=raw_password)  
            if user is not None:
                login(request, user)
                return redirect('profile-update')  # 회원가입 성공 시 이동할 URL
        else:
            # 폼 유효성 검사 실패 시 오류 메시지를 포함하여 다시 렌더링
            messages.error(request, '회원가입에 실패했습니다. 입력한 정보를 다시 확인해주세요.')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})



class IndexView(View):
    def get(self, request): 
        return render(request, 'posts/index.html')
# 나중에 메인 페이지에 값을 추가할려면 여기다 추가하면 됨 context에 담아서 
    



class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'posts/profile_update_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})
# get_success 는 이 페이지가 끝나면 profile이라는 이름을 가진 html로 감 
# kwargs 는 reverse 될 때 user_id 값을 가지고 가라는 뜻 url에서 <user_id> 이런식으로 만드니
# 해당 유저 페이지로 가야되니 
class ProfileView(DetailView):
    model = User
    template_name = 'posts/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'
    # 템플리세에서 참조할 수 잇는거 만약에 추가로 다른 모델에서 가져와서 
    # 추가해야되면 밑에 get_context_data 가져와야 됨 
 #   def get_context_data(self, **kwargs):
     #   context = super().get_context_data(**kwargs)
      #  user = self.request.user
       # profile_user_id = self.kwargs.get('user_id')
        #if user.is_authenticated :
         #   context['is_following']=user.following.filter(id=profile_user_id).exists()
        #context['user_reviews'] = Review.objects.filter(author_id=profile_user_id)[:4]
        #return context 
class ProfileEditView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'posts/profile_edit.html'
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})
    
class PasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('profile',kwargs={'user_id':self.request.user.id})
