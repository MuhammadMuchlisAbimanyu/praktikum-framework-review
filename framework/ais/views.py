from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentsForm
from .models import Students
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .decorators import group_required

# Create your views here.
def homepage(request):
    context = {
        'home' : True
    }
    return render(request, 'homepage/index.html', context)

def about(request):
    context = {
        'about' : True
    }
    return render(request, 'homepage/about.html', context)

# READ Mahasiswa
def student_index(request):
    students = Students.objects.all()
    return render(request, 'student/index.html', {'students': students})

def student_create(request):
    if request.method == 'POST':
        form = StudentsForm(request.POST)
        if form.is_valid():
            form.save()  # Simpan data mahasiswa ke database
            messages.success(request, 'Mahasiswa berhasil dibuat!')  # Pesan sukses
            return redirect('student_index')  # Redirect ke halaman index mahasiswa
    else:
        form = StudentsForm()  # Definisikan form jika metode bukan POST
    return render(request, 'student/create.html', {'form': form})

# UPDATE Mahasiswa
def student_update(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    if request.method == 'POST':
        form = StudentsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data mahasiswa berhasil diubah!')
            return redirect('student_index')
    else:
        form = StudentsForm(instance=student)
    return render(request, 'student/update.html', {'form': form, 'student': student})

# DELETE Mahasiswa
def student_delete(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    student.delete()
    messages.success(request, 'Data mahasiswa berhasil dihapus')
    return JsonResponse({'success': True})

@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif user.groups.filter(name='Student').exists():
        return redirect('dashboard_student')
    elif user.groups.filter(name='Teacher').exists():
        return redirect('dashboard_teacher')
    return HttpResponseForbidden("You do not have permission to access this page.")

@login_required
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@login_required
def dashboard_student(request):
    return render(request, 'dashboard/student.html')

@login_required
def dashboard_teacher(request):
    return render(request, 'dashboard/teacher.html')

@group_required('Admin')
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@group_required('Student')
def dashboard_student(request):
    return render(request, 'dashboard/student.html')

@group_required('Teacher')
def dashboard_teacher(request):
    return render(request, 'dashboard/teacher.html')
