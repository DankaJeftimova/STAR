from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from  django.contrib.auth import login, logout
from django import forms
from .models import ClassModel, Question, Quiz, Lecture, SubmitQuiz, Announcement
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



class NewClass(forms.ModelForm):
    class Meta:
        model = ClassModel
        fields = ['name', 'description', 'tags']
        widgets = {
            
            'tags': forms.CheckboxSelectMultiple(),
        }


class Search(forms.Form):
    title = forms.CharField(label="title")


def index(request):
    user_classes = ClassModel.objects.filter(author=request.user)

    enrolled_classes = request.user.enrolled_classes.all()

    other_user_classes = ClassModel.objects.exclude(author=request.user).exclude(students=request.user)

    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
    
            found = ClassModel.objects.filter(name__icontains=title)

            return render(request, "classes/search_result.html", {
                "user_classes": found,
                "other_user_classes": other_user_classes,
                "enrolled_classes": enrolled_classes,
                "form": Search(),
            })

    return render(request, "classes/index.html", {
        "user_classes": user_classes,
        "other_user_classes": other_user_classes,
        "enrolled_classes": enrolled_classes,
        "form": Search(),
    })
    



@login_required
def create_class(request):
        if request.method == "POST":
            form = NewClass(request.POST)
            if form.is_valid():
                current=form.save(commit=False)
                current.author = request.user
                current.save()
                form.save_m2m()
                return redirect("classes:index")
        else:
            form = NewClass()

        return render(request, 'classes/create_class.html',{
            "form": form,
        })


@login_required
def manage_class(request, pk):
    class_obj = get_object_or_404(ClassModel, pk=pk)
    
    quizzes = class_obj.quizzes.all().order_by('-created_at')

    if request.method == "POST":
        action = request.POST.get('manage')

        if action == 'delete':
            return redirect('classes:last_check', pk=pk)

        if action == 'change':
            class_obj.name = request.POST.get('name')
            class_obj.description = request.POST.get('description')
            class_obj.save()
            return redirect('classes:manage_class', pk=pk)

        if action == 'create_quiz_container':
            title = request.POST.get('quiz_title')
            due_date_raw = request.POST.get('due_date') 

            if not due_date_raw:
                due_date_raw = None

            if title:
                Quiz.objects.create(course=class_obj, title=title, due_date = due_date_raw)
            return redirect('classes:manage_class', pk=pk)

        if action == 'toggle_quiz':
            quiz_id = request.POST.get('quiz_id')
            quiz = get_object_or_404(Quiz, id=quiz_id, course=class_obj)
            quiz.is_published = not quiz.is_published
            quiz.save()
            return redirect('classes:manage_class', pk=pk)

        if action == 'add_question':
            quiz_id = request.POST.get('quiz_id')
            target_quiz = get_object_or_404(Quiz, id=quiz_id, course=class_obj)
            
            Question.objects.create(
                quiz=target_quiz,  
                prompt=request.POST.get('question_prompt'),
                option_a=request.POST.get('option_a'),
                option_b=request.POST.get('option_b'),
                option_c=request.POST.get('option_c'),
                option_d=request.POST.get('option_d'),
                answer=request.POST.get('correct_choice')
            )
            return redirect('classes:manage_class', pk=pk)

        if action == 'delete_question':
            question_id = request.POST.get('question_id')
            question_to_delete = get_object_or_404(Question, id=question_id, quiz__course=class_obj)
            question_to_delete.delete()
            return redirect('classes:manage_class', pk=pk)
        
        if action == 'delete_quiz':
            quiz_id = request.POST.get('quiz_id')
            quiz_to_delete = get_object_or_404(Quiz, id=quiz_id)
            quiz_to_delete.delete()
            return redirect('classes:manage_class', pk=pk)

       
        if action == 'update_quiz_meta':
            quiz_id = request.POST.get('quiz_id')
            quiz = get_object_or_404(Quiz, id=quiz_id, course=class_obj)
            quiz.title = request.POST.get('edit_quiz_title')
            due_date = request.POST.get('edit_due_date')
            quiz.due_date = due_date if due_date else None
            quiz.save()
            return redirect('classes:manage_class', pk=pk)

        if action == 'update_question':
            q_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=q_id, quiz__course=class_obj)
            question.prompt = request.POST.get('edit_prompt')
            question.option_a = request.POST.get('edit_a')
            question.option_b = request.POST.get('edit_b')
            question.option_c = request.POST.get('edit_c')
            question.option_d = request.POST.get('edit_d')
            question.answer = request.POST.get('edit_correct')
            question.save()
            return redirect('classes:manage_class', pk=pk)

        if action == 'add_lecture':
            title = request.POST.get('lecture_title')
            content = request.POST.get('lecture_content')
            link = request.POST.get('lecture_link')
            
            new_lecture = Lecture.objects.create(
                course=class_obj,
                title=title,
                content=content,
                external_link=link
            )
            
            if 'lecture_video' in request.FILES:
                new_lecture.video_file = request.FILES['lecture_video']
            
            if 'file_1' in request.FILES:
                new_lecture.file_1 = request.FILES['file_1']
            if 'file_2' in request.FILES: 
                new_lecture.file_2 = request.FILES['file_2']
            if 'file_3' in request.FILES: 
                new_lecture.file_3 = request.FILES['file_3']
            if 'file_4' in request.FILES: 
                new_lecture.file_4 = request.FILES['file_4']
            if 'file_5' in request.FILES: 
                new_lecture.file_5 = request.FILES['file_5']
            
            new_lecture.save()
            return redirect('classes:manage_class', pk=pk)

        if action == 'delete_lecture':
            lec_id = request.POST.get('lecture_id')
            lec_del =  get_object_or_404(Lecture, id=lec_id)
            lec_del.delete()
            return redirect('classes:manage_class', pk=pk)
        
        if action == "add_announcement":
            title = request.POST.get('announcement_title')
            body = request.POST.get('announcement_body')
            
            is_live = 'is_live' in request.POST 
            
            Announcement.objects.create(
                classroom=class_obj,
                title=title,
                body=body,
                is_live=is_live,
                author=request.user
            )
        
        elif action == "toggle_announcement":
            a_id = request.POST.get('announcement_id')
            announcement = Announcement.objects.get(id=a_id, classroom=class_obj)
            announcement.is_live = not announcement.is_live
            announcement.save()

        elif action == "delete_announcement":
            a_id = request.POST.get('announcement_id')
            Announcement.objects.filter(id=a_id, classroom=class_obj).delete()


        if action == "update_lecture":
            l_id = request.POST.get('lecture_id')
            lecture = get_object_or_404(Lecture, id=l_id)
            
            lecture.title = request.POST.get('edit_title')
            lecture.content = request.POST.get('edit_content')
            lecture.link = request.POST.get('edit_link')
            
            for i in range(1, 6):
                file_key = f'file_{i}'
                if file_key in request.FILES:
                    setattr(lecture, file_key, request.FILES[file_key])
            
            if 'lecture_video' in request.FILES:
                lecture.video_file = request.FILES['lecture_video']
                
            lecture.save()
            return redirect('classes:manage_class', pk=pk)

        
        
            

    quizzes = Quiz.objects.filter(course=class_obj)
    students = class_obj.students.all()

    submissions = SubmitQuiz.objects.filter(quiz__course=class_obj)

   
    all_data = {}

    for student in students:
        all_data[student.username] = [
        ["Student username", "Quiz", "Correct answers", "Incorrect answers", "Date submited", "Punctuality"]
    ]

    for sub in submissions:
        name = sub.student.username

        tab = all_data.get(name)

   
        if tab is not None:
            if sub.date <= sub.quiz.due_date:
                punc = "On time"
            else:
                punc = "Late"

            tab.append([name, sub.quiz.title, sub.score, sub.quiz.questions.count() - sub.score, sub.date, punc])
        
        else:
            continue
        

    
    
    
 

    return render(request, 'classes/manage_class.html', {
        'class_obj': class_obj,
        'quizzes': quizzes,
        'students': class_obj.students.all(),
        'lectures': class_obj.lectures.all(),
        'dictionary' : all_data,
        'announcements': class_obj.announcements.all(),
        
    })


@login_required
def enroll(request, pk):
    classjoin = get_object_or_404(ClassModel, pk=pk)
    classjoin.students.add(request.user)
    return redirect('classes:index')



@login_required
def last_check(request, pk):
    class_obj = get_object_or_404(ClassModel, pk=pk)

    if request.method == "POST":
        action = request.POST.get('confirmation')

        if action == "yes":
            class_obj.delete()
            return redirect('classes:index')
        
    return render(request, 'classes/last_check.html',{
        'class_obj': class_obj,
    })



@login_required
def continue_learning(request, pk):
    class_obj = get_object_or_404(ClassModel, pk=pk)
    
    lectures = Lecture.objects.filter(course=class_obj).order_by('-created_at')

    if request.method == 'POST':
  
        if request.POST.get('action') == 'unenroll':
            class_obj.students.remove(request.user)
            return redirect('classes:index')
    
    submissions_qs = SubmitQuiz.objects.filter(
        student=request.user,
        quiz__course=class_obj 
    ).select_related('quiz')

    submitted_ids = list(submissions_qs.values_list('quiz_id', flat=True))

    context = {
        'class_obj': class_obj,
        'lectures': lectures,
        'submissions': submissions_qs,
        'submitted_quiz_ids': submitted_ids, 
        'announcements': class_obj.announcements.all(),
    }
    
    return render(request, 'classes/continue_learning.html', context)


@login_required
def take_quiz(request, pk):
    quiz_to_show = get_object_or_404(Quiz, pk=pk)

    return render(request, 'classes/take_quiz.html', {
        "questions": quiz_to_show.questions.all(),
        "quiz": quiz_to_show,
    } )


@login_required
def submit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()
    score = 0
    total = questions.count()

    if request.method == 'POST':
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            
            if user_answer == question.answer:
                score += 1

        
        SubmitQuiz.objects.create(
            student=request.user,
            quiz=quiz,
            score=score
        )

    return render(request, 'classes/submited.html',{
        "score" : score,
        "total": total,
        "quiz": quiz,
    })


@login_required
def log_out(request):
    if request.method == "POST":
        logout(request)
        return render(request, "accounts/base.html")
    
    return render("classes:index")




@login_required
def profile_settings(request, pk):
    return render(request, 'classes/profile_settings.html')



@login_required
def dismiss(request, class_pk, user_pk):
    if request.method == 'POST':
        course = get_object_or_404(ClassModel, id=class_pk)
        student = get_object_or_404(User, id=user_pk)
        
        
        course.students.remove(student)
        
    
    return redirect('classes:manage_class', pk=class_pk)