from django.http import *
from django.shortcuts import render, redirect
from .models import Book,Author,BookInstance#, Genre, Group, Student, Lecturer, Course
from django.views import generic
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthorsForm
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from .models import *
from django.urls import reverse_lazy

#
# # Create your views here.
class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
class DeleteBook(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

def edit1(request,id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")
    else:
        return render(request, "catalog/edit1.html", {"author": author})
def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add/")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Author not found</h2>")

def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")

def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, 'catalog/authors_add.html',
                  {'form': authorsform, 'author': author})

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user).filter(
            status__exact='1').order_by('due_back')
#

# def home(request):
#     groups = Group.objects.all()
#     return render(request, "catalog/home.html", {"groups": groups})
#
#
# def groups(request):
#     groups = Group.objects.all()
#     return render(request,"catalog/groups.html",{"groups": groups})
#
#
# def group(request, id):
#     group = Group.objects.get(id=id)
#     return render(request, "catalog/group.html", {"group": group})
#
#
# def students(request):
#     students = Student.objects.all()
#     return render(request, "catalog/students.html", {"students": students})
#
#
# def student(request, id):
#     student = Student.objects.get(id=id)
#     return render(request, "catalog/student.html", {"student": student})
#
#
# def lecturers(request):
#     lecturers = Lecturer.objects.all()
#     return render(request, "catalog/lecturers.html", {"lecturers": lecturers})
#
#
# def lecturer(request, id):
#     lecturer = Lecturer.objects.get(id=id)
#     courses = Course.objects.filter(lecturer=lecturer)
#
#     return render(
#         request,
#         "catalog/lecturer.html",
#         {
#             "lecturer": lecturer,
#             "courses": courses
#         }
#     )
#
class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4

def index(request):
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
    num_instance_available = BookInstance.objects.filter(status__exact=2).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits+1

    return render(request, 'index.html',
                  context={
                      'num_books':num_books,
                      'num_instance':num_instance,
                      'num_instance_available':num_instance_available,
                      'num_authors':num_authors,
                      'num_visits':num_visits,
                  })
