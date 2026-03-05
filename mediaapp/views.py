import random
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Media

import cloudinary
import cloudinary.uploader


# Cloudinary configuration
cloudinary.config(
    cloud_name="dnheyv7vz",
    api_key="793549159378729",
    api_secret="6ZIS7tFJYeGwL_VWxK0TsvODJSA"
)


# Generate random share code
def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        # Prevent duplicate usernames
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(username=username, password=password)

        messages.success(request, "Account created successfully")

        return redirect("login")

    return render(request, "register.html")


# ---------------- LOGIN ----------------

def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:

            login(request, user)

            return redirect("dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# ---------------- LOGOUT ----------------

def logout_view(request):

    logout(request)

    return redirect("login")


# ---------------- DASHBOARD ----------------

@login_required
def dashboard(request):

    texts = Media.objects.filter(user=request.user, type="text")
    images = Media.objects.filter(user=request.user, type="image")
    videos = Media.objects.filter(user=request.user, type="video")

    return render(request, "dashboard.html", {
        "texts": texts,
        "images": images,
        "videos": videos,
        "username": request.user.username
    })


# ---------------- UPLOAD ----------------

@login_required
def upload(request):

    if request.method == "POST":

        text = request.POST.get("text")
        file = request.FILES.get("file")

        if file:

            # VIDEO upload
            if file.content_type.startswith("video/"):

                result = cloudinary.uploader.upload_large(
                    file,
                    resource_type="auto",
                    chunk_size=6000000
                )

                Media.objects.create(
                    user=request.user,
                    type="video",
                    file_url=result["secure_url"]
                )

            # IMAGE upload
            else:

                result = cloudinary.uploader.upload(
                    file,
                    resource_type="image"
                )

                Media.objects.create(
                    user=request.user,
                    type="image",
                    file_url=result["secure_url"]
                )

        else:

            Media.objects.create(
                user=request.user,
                type="text",
                text_content=text
            )

        return redirect("dashboard")

    return render(request, "upload.html")


# ---------------- GENERATE LINK ----------------

@login_required
def generate_link(request, id):

    media = get_object_or_404(Media, id=id, user=request.user)

    if not media.share_code:

        media.share_code = generate_code()
        media.save()

    return redirect("dashboard")


# ---------------- DELETE MEDIA ----------------

@login_required
def delete_media(request, id):

    media = get_object_or_404(Media, id=id, user=request.user)

    media.delete()

    return redirect("dashboard")


# ---------------- VIEW SHARE ----------------

def view_share(request, code):

    media = Media.objects.filter(share_code=code).first()

    return render(request, "view_share.html", {"media": media})
def home(request):
    return render(request, "home.html")