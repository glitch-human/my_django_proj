from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# # Create your models here.



# class Lecturer(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Student(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Group(models.Model):
#     name = models.CharField(max_length=100)
#     lecturer = models.ForeignKey(
#         Lecturer,
#         on_delete=models.CASCADE
#     )
#     students = models.ManyToManyField(Student)
#
#     def __str__(self):
#         return self.name
#
#
# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     lecturer = models.ForeignKey(
#         Lecturer,
#         on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return self.name



class Genre(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter Book genre",
                            verbose_name="Book genre")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20,
                            help_text="Enter Book language",
                            verbose_name="Book language")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(
        max_length=100,
        help_text="Enter author's name",
        verbose_name="Author's name"
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Enter author's lastname",
        verbose_name="Author's lastname"
    )
    date_of_birth = models.CharField(
        max_length=100,
        help_text="Enter author's date of birth",null=True,blank=True,
        verbose_name="Date of birth"
    )
    date_of_death = models.CharField(
        max_length=100,
        help_text="Enter author's date of death",null=True,blank=True,
        verbose_name="Date of death")

    def __str__(self):
        return self.last_name

class Book(models.Model):
    title = models.CharField(max_length=200,
                             help_text="Enter book name",
                             verbose_name="Book name")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text="Choose genre for a book",
                              verbose_name="Book genre", null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 help_text="Choose language for a book",
                                 verbose_name="Book language",null=True,)
    author = models.ManyToManyField('Author',
                                    help_text="Choose book author",
                                    verbose_name="Book author")
    summary = models.TextField(max_length=1000,
                               help_text="Enter a short description of the book",
                               verbose_name="Book's summary")
    isbn = models.CharField(max_length=13,
                            help_text="Must contain 13 charachters",
                            verbose_name="Book's ISBN")

    def __str__(self):
        return self.title
    def display_author(self):
        return ','.join([author.last_name for author in self.author.all()

        ])
    display_author.short_description = 'Authors'
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class Status(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter status of the book copy",
                            verbose_name="Book copy status")
    def __str__(self):
        return self.name

class BookInstance(models.Model):
    book = models. ForeignKey ('Book',on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text="Enter the book inventory number",
                               verbose_name="Book inventory number")
    imprint = models.CharField(max_length=200,
                               help_text="Enter the publisher and year of publication",
                               verbose_name="Publisher")

    status = models. ForeignKey('Status', on_delete=models.CASCADE,
                                null=True,
                                help_text='Change the status of the copy',
                                verbose_name="Book copy status")
    due_back = models.DateField(null=True, blank=True,
                                help_text="Enter the end of the status period",
                                verbose_name="Status expiration date")

    borrower = models.ForeignKey(User,on_delete=models.SET_NULL
                                 , null=True,blank=True,
                                 help_text="Select the book's client",
                                 verbose_name="Client")
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
