from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from .forms import ProfileForm, CASignupForm
from .models import Profile, Session
from .forms import User

def index(request):
    return render(request, "index.html")

class ProfileView(View):
    initial = {'key': 'value'}
    template_name = 'profile_view.html'

    def get(self, request, *args, **kwargs):
        try:
            self.profile_user = User.objects.get(username=kwargs.get("profile_user"))
        except Exception:
            self.error = "User {id} not existed.".format(id=kwargs.get("profile_user"))
            self.profile_user = None
            return render(request, "404.html", {})


        try:
            self.profile_info = Profile.objects.get(user=self.profile_user)
        except Exception:
            self.profile_info = None

        res = {
            "user": self.profile_user,
            "profile": self.profile_info
        }
        return render(request, self.template_name, res)

    def post(self, request, *args, **kwargs):
        # Unauthorized modification
        try:
            self.profile_user = User.objects.get(username=kwargs.get("profile_user"))
        except Exception:
            self.error = "User {id} not existed.".format(id=kwargs.get("profile_user"))
            self.profile_user = None
            raise render(request, "404.html", {})

        try:
            self.profile_info = Profile.objects.get(user=self.profile_user)
        except Exception:
            self.profile_info = None

        if self.profile_user != request.user:
            raise PermissionDenied

        bio = request.POST.get("bio", None)
        avatar = request.FILES.get("avatar", None)

        if self.profile_info:
            self.profile_info.bio = bio
            if avatar:
                self.profile_info.avatar = avatar
            self.profile_info.save()
        else:
            self.profile_info = Profile(user=request.user, bio=bio, avatar=avatar)
            form = ProfileForm(request.POST, request.FILES, instance=self.profile_info)

            if form.is_valid():
                print ("valid")
                self.profile_info.save()
            else:
                print (form.errors)

        res = {
            "user": self.profile_user,
            "profile": self.profile_info
        }
        return render(request, self.template_name, res)


class LoginView(View):
    initial = {'active_page': 'register'}
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "active_page": "login",
            "error": None
        })

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/lobby")

            else:
                res = {'active_page': 'login',
                       "error": "Inactive user."}
                return render(request, self.template_name, res)
        else:
            res = {'active_page': 'login',
                   "error": "Invalid username or password."}
            return render(request, self.template_name, res)


def lobby(request):
    if request.method == "POST":
        room_code = request.POST.get("room_code")
        char_choice = request.POST.get("character_choice")
        return redirect(
            '/play/%s?&choice=%s'
            %(room_code, char_choice)
        )
    if request.method == "GET":
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Exception:
            profile = None
        return render(request, "lobby.html", {
            "user": {
                "name": user.username,
                "avatar": profile.avatar.url if profile else ""
            }
        })


def game(request, room_code):
    choice = request.GET.get("choice")
    if choice not in ['X', 'O']:
        raise Http404("Choice does not exists")
    context = {
        "char_choice": choice,
        "room_code": room_code
    }
    return render(request, "game.html", context)


class CaUserSignupView(CreateView):
    model = User
    form_class = CASignupForm
    template_name = 'causer_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/lobby')
