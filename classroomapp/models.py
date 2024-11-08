from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class googleclass(models.Model):
    Name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='classinstructor')

    def __str__(self):
        return self.Name
    

class student(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='class_student')
    profilepic = models.ImageField(upload_to='images/', null=True, blank=True)
    students = models.ForeignKey(googleclass, on_delete=models.CASCADE, null=True, blank=True, related_name='classinstructor')
    
    def __str__(self):
        return self.name.username

class classdata(models.Model):
    name = models.ForeignKey(googleclass, on_delete=models.CASCADE, null=True, blank=True, related_name='class_material')
    lecture = models.FileField(upload_to='resource/', blank=True, null=True)
    message = models.CharField(max_length=1000, blank=True, null=True)

    
    def __str__(self):
        return self.message

class assignment(models.Model):
    name = models.ForeignKey(googleclass, on_delete=models.CASCADE, null=True, blank=True, related_name='std_assignment')
    content = models.FileField(upload_to='resource/', blank=True, null=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    start_date = models.DateField()
    due_date = models.DateField()

    
    def __str__(self):
        return self.message
    
class uploadassignment(models.Model):
    name = models.ForeignKey(assignment, on_delete=models.CASCADE, blank=True, related_name='upload_assignment')
    studentname = models.ForeignKey(student, on_delete=models.CASCADE, blank=True)
    content = models.FileField(upload_to='resource/')
    submission_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.studentname.name.username