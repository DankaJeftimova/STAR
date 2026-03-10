from django.contrib import admin
from .models import ClassModel, Tag, Question, Quiz, Lecture, SubmitQuiz

admin.site.register(ClassModel)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Lecture)
admin.site.register(SubmitQuiz)

