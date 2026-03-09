from django.shortcuts import render,redirect
from .models import Student,Book,Borrow
from datetime import date,timedelta


def students(request):

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']

        Student.objects.create(name=name,email=email)

        return redirect('/students')

    data = Student.objects.all()

    return render(request,'students.html',{'students':data})


def books(request):

    if request.method == "POST":

        title = request.POST['title']
        author = request.POST['author']

        Book.objects.create(title=title,author=author)

        return redirect('/books')

    data = Book.objects.all()

    return render(request,'books.html',{'books':data})


def issue_book(request):

    students = Student.objects.all()
    books = Book.objects.filter(available=True)

    message = ""

    if request.method == "POST":

        student_id = request.POST['student']
        book_id = request.POST['book']

        student = Student.objects.get(id=student_id)
        book = Book.objects.get(id=book_id)

        count = Borrow.objects.filter(student=student,returned=False).count()

        if count >= 3:
            message = "Student already has 3 books"

        elif book.available == False:
            message = "Book already taken"

        else:

            due = date.today() + timedelta(days=14)

            Borrow.objects.create(
                student=student,
                book=book,
                due_date=due
            )

            book.available = False
            book.save()

            return redirect('/issue')

    return render(request,'issue.html',{
        'students':students,
        'books':books,
        'message':message
    })


def return_book(request):

    records = Borrow.objects.filter(returned=False)

    if request.method == "POST":

        borrow_id = request.POST['borrow']

        record = Borrow.objects.get(id=borrow_id)

        record.returned = True
        record.return_date = date.today()
        record.save()

        book = record.book
        book.available = True
        book.save()

        return redirect('/return')

    return render(request,'return.html',{'records':records})


def report(request):

    data = Borrow.objects.all()

    if request.method == "POST":

        f = request.POST['from']
        t = request.POST['to']

        data = Borrow.objects.filter(
            borrow_date__range=[f,t]
        )

    return render(request,'report.html',{'data':data})