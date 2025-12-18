from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from quiz.models.quiz import Quiz


def admin_login_view(request):
    """
    Simple username/password login for quiz admin portal.
    Uses Django's built-in User model. User must be staff.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("quiz:admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
        elif not user.is_staff:
            messages.error(request, "You do not have admin access to this portal.")
        else:
            login(request, user)
            return redirect("quiz:admin_dashboard")

    return render(request, "admin/admin_login.html")


@staff_member_required
def admin_logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("quiz:admin_login")


@staff_member_required
def admin_dashboard_view(request):
    """
    Central dashboard for quiz admins:
    - See all quizzes
    - Quick links to create/edit/delete
    - Links to results & certificates
    """
    quizzes = Quiz.objects.all().order_by("-created_at")

    return render(
        request,
        "admin/admin_dashboard.html",
        {
            "quizzes": quizzes,
        },
    )


