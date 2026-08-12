from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer

def signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        mobile = request.POST.get("mobile", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        ctx = {"full_name": full_name, "email": email, "mobile": mobile}

        if not full_name:
            messages.error(request, "Please enter your full name.")
            return render(request, "signup.html", ctx)

        if not email:
            messages.error(request, "Please enter your email address.")
            return render(request, "signup.html", ctx)

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "signup.html", ctx)

        if not mobile:
            messages.error(request, "Please enter your mobile number.")
            return render(request, "signup.html", ctx)

        if not password1:
            messages.error(request, "Please enter a password.")
            return render(request, "signup.html", ctx)

        if len(password1) < 8:
            messages.error(request, "Password must contain at least 8 characters.")
            return render(request, "signup.html", ctx)

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html", ctx)

        customer = Customer.objects.create(
            full_name=full_name,
            email=email,
            mobile=mobile,
            password=make_password(password1)
        )
        request.session["customer_id"] = customer.id
        return redirect("dashboard")

    return render(request, "signup.html")

def login_view(request):
    login_error = None
    if request.method == "POST":
        email = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        try:
            customer = Customer.objects.get(email=email)
            if check_password(password, customer.password):
                request.session["customer_id"] = customer.id
                return redirect("dashboard")
            else:
                login_error = "Invalid email or password."
        except Customer.DoesNotExist:
            login_error = "Invalid email or password."

    return render(request, "login.html", {"login_error": login_error})

def logout_view(request):
    request.session.flush()
    return redirect("login")

def dashboard(request):
    customer_id = request.session.get("customer_id")
    customer = Customer.objects.filter(id=customer_id).first() if customer_id else None
    return render(request, "dashboard.html", {"customer": customer})

def profile_view(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")
    return render(request, "profile.html", {"customer": customer})

def edit_profile(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")

        if Customer.objects.filter(email=email).exclude(id=customer.id).exists():
            messages.error(request, "This email address is already registered.")
            return render(request, "edit_profile.html", {"customer": customer})

        customer.full_name = full_name
        customer.email = email
        customer.mobile = mobile
        customer.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect("profile")

    return render(request, "edit_profile.html", {"customer": customer})

def change_password(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not check_password(current_password, customer.password):
            messages.error(request, "Your current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("change_password")

        if check_password(new_password, customer.password):
            messages.error(request, "New password must be different from your current password.")
            return redirect("change_password")

        customer.password = make_password(new_password)
        customer.save()
        messages.success(request, "Your password has been changed successfully.")
        return redirect("profile")

    return render(request, "change_password.html", {"customer": customer})

def delete_account(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")

    if request.method == "POST":
        customer.delete()
        request.session.flush()
        return redirect("login")

    return render(request, "delete_account.html", {"customer": customer})