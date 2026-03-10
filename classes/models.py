from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    


class ClassModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="classes")
    students = models.ManyToManyField(User, related_name="enrolled_classes", blank=True)

    def __str__(self):
        return self.name
    


class Quiz(models.Model):
    course = models.ForeignKey(ClassModel, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"
    


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    prompt = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    answer = models.CharField(max_length=1) 




class Lecture(models.Model):
    course = models.ForeignKey(ClassModel, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    
    video_file = models.FileField(upload_to='lectures/videos/', blank=True, null=True)
    
    file_1 = models.FileField(upload_to='lectures/docs/', blank=True, null=True)
    file_2 = models.FileField(upload_to='lectures/docs/', blank=True, null=True)
    file_3 = models.FileField(upload_to='lectures/docs/', blank=True, null=True)
    file_4 = models.FileField(upload_to='lectures/docs/', blank=True, null=True)
    file_5 = models.FileField(upload_to='lectures/docs/', blank=True, null=True)
    
    external_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_count(self):
        files = [self.file_1, self.file_2, self.file_3, self.file_4, self.file_5]
        return len([f for f in files if f])

    def __str__(self):
        return self.title
    


class SubmitQuiz(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)




class Announcement(models.Model):
    
    classroom = models.ForeignKey(
        ClassModel, 
        on_delete=models.CASCADE, 
        related_name='announcements'
    )
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_live = models.BooleanField(default=True)
    
  
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True
    )


    def __str__(self):
        return f"{self.title} - {self.classroom.name}"