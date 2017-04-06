from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django import forms
from .models import Venue, Artist, Note, Show, UserProfile
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserProfileForm, UserProfileEditForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone



def user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    userP= UserProfile.objects.get(user = user)
    #userProfile_pk=userP.user.pk
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    return render(request, 'lmn/users/user_profile.html', {'user' : user , 'userProfile':userP, 'notes' : usernotes })
    #return redirect('lmn:my_user_profile', userProfile_pk)
    #return redirect ('my_user_profile', pk=user_pk)
    #my_user_profile(request.POST, user_pk)

#     return redirect(request.POST, 'my_user_profile' )
#     user = User.objects.get(pk=user_pk)
#     userProfile = UserProfile.objects.get(user = user)
#     usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
#     return render(request, 'lmn/users/user_profile.html', {'user' : user , 'userProfile':userProfile, 'notes' : usernotes })



@login_required
def my_user_profile(request, user_pk):
    #def post_edit(request, pk):
    user = get_object_or_404(User, pk=user_pk)
    userP= UserProfile.objects.get(user = user)
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    form = UserProfileEditForm(request.POST)
    if request.method == "POST":

        if form.is_valid():
            userPNone = form.save(commit=False)
            print(form.cleaned_data)

            userP.about = userPNone.about
            print(userP.about)
            print(userPNone.about)


            userP.save()
            print(userP)
            return render(request, 'lmn/users/user_profile.html', {'user' : user , 'userProfile':userP, 'notes' : usernotes })
        else:
            #form = UserProfileEditForm()
            return render("lmn/users/orcamento.html", {"form": form })

    # Get request to edit user profile
    else:
        form = UserProfileEditForm(instance=userP)
        return render(request, 'lmn/users/my_user_profile.html', {'form': form, 'user' : user , 'userProfile':userP } )
    # if request.method == "POST":
    #
    #     form = UserProfileForm(request.POST, instance=userP)
    #     if form.is_valid():
    #         upedit = form.save(commit=False)
    #         upedit.save()
    #         return render(request, 'lmn/users/my_user_profile.html', {'form': form, 'user' : user , 'userProfile':userP, 'notes' : usernotes })
    # else:
    #
    #     return render(request, 'lmn/users/my_user_profile.html', { 'user' : user , 'userProfile':userP, 'notes' : usernotes })

    # user = User.objects.get(pk=user_pk)
    # userP = UserProfile.objects.get(user = user)
    # if request.method == 'POST' :
    #
    #     form = UserProfileForm(request.POST)
    #     if form.is_valid():
    #
    #         userPro = form.save(commit=False);
    #
    #         userPro.about = about
    #
    #         userPro.save()
    #         return redirect('lmn:note_detail', user_username=note.pk)
    #
    # else :
    #     form = NewNoteForm()
    # TODO - editable version for logged-in user to edit own profile
    # return render(request, 'lmn/users/user_profile.html', user_pk=request.user.pk)
# @login_required
# def my_user_profile(request):
#     user = User.objects.get(pk=user_pk)
#     userProfile = UserProfile.objects.get(user = user)
#     form = UserProfileForm(userProfile)
#     usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
#     return render(request, 'lmn/users/profile_edit.html', {'user' : user , 'userProfile':userProfile, 'notes' : usernotes })


def register(request):

    if request.method == 'POST':


        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
            login(request, user)
            # userProfile = UserProfileForm(request.POST)
            # userProfile.user = user
            # userProfile.joined_date = timezone.now()
            # userProfile.save()

            if request.user.is_authenticated():  # If userprofile object has a user object property
                userP = UserProfile(user = user, about = '', joined_date=timezone.now())

                userP.save()

                return render(request, 'lmn/users/user_profile.html', {'form': form, 'user' : user , 'userProfile':userP, 'notes' : usernotes })

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )


    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form' : form } )


def logout_view(request):
    response = logout(request)
    message = 'You have been logged out\n Goodbye!'
    return render(request, 'registration/logout.html', {'message':message})
