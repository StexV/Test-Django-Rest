from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render

from blog.models import Article

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def post(request):
    context = {
        'posts': Article.objects.filter(author=request.user)
    }

    return render(request, 'home.html', context)