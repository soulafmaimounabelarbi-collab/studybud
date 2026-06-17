from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Content, Feedback  # 👈 نستورد Profile
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def loginPage(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Username or password incorrect")
            return redirect('login')

        profile = user.profile  # 👈 نحصل على Profile المرتبط بالمستخدم

        # 🔐 منع الأستاذ إذا لم يتم قبول حسابه
        if profile.role == "teacher" and profile.state != "approved":
            messages.error(request, "Your account is pending admin approval.")
            return redirect("login")

        # 🔐 تسجيل الدخول
        login(request, user)

        # 🔀 إعادة التوجيه حسب الدور
        if profile.role == 'admin':
            return redirect('admin-dashboard')

        elif profile.role == 'teacher':
            return redirect('teacher-dashboard')

        elif profile.role == 'student':
            return redirect('student-dashboard')

        return redirect('home')

    return render(request, 'login.register.html', {})



def logoutUser(request):
    logout(request)
    return redirect('home')



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    context = {'rooms': rooms}
    return render(request, 'home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'room.html', {'room': room})



@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
         form.save()
        return redirect('home')
    return render(request, 'room_form.html', {'form': form})



def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'room_form.html', {'form': form})



def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': room})



# ===================== DASHBOARDS =========================

def studentDashboard(request):
    if request.user.profile.role != 'student':
        return redirect('home')
    return render(request, "student.html")


def teacherDashboard(request):
    if request.user.profile.role != 'teacher':
        return redirect('home')
    return render(request, "teacher.html")


def adminDashboard(request):
    if request.user.profile.role != 'admin':
        return redirect('home')

    # 👇 عرض لائحة الأساتذة Pending
    pending_teachers = Profile.objects.filter(role="teacher", state="pending")

    return render(request, "admin.html", {"pending_teachers": pending_teachers})

def approveTeacher(request, pk):
    if request.user.profile.role != 'admin':
        return redirect('home')

    teacher = Profile.objects.get(user__id=pk)
    teacher.state = "approved"
    teacher.save()

    messages.success(request, "Teacher approved successfully!")
    return redirect("admin-dashboard")

