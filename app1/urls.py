from django.urls import path
from . import views

urlpatterns = [

path('',views.students),

path('students/',views.students),
path('books/',views.books),
path('issue/',views.issue_book),
path('return/',views.return_book),
path('report/',views.report),

]