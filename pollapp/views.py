from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    questions = Question.objects.all()
    return render(request, 'pollapp/index.html', {'questions': questions})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'pollapp/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        choice_id = request.POST.get('choice')
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pollapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a valid choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return redirect('pollapp:results', question_id=question.id)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'pollapp/results.html', {'question': question})


@login_required
def create(request):
    if request.method == "POST":
        question_text = request.POST.get('question')
        choices = request.POST.getlist('choices')

        if question_text:
            # ✅ ADD user=request.user HERE
            question = Question.objects.create(
                question_text=question_text,
                user=request.user
            )

            for choice_text in choices:
                if choice_text.strip():  # ignore empty inputs
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text
                    )

            return redirect('pollapp:index')

    return render(request, 'pollapp/create.html')


def login_view(request):
    return render(request, 'pollapp/login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('pollapp:index')

    return render(request, 'pollapp/register.html')

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # 🔐 permission
    if request.user != question.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit this question.")
        return redirect('pollapp:index')

    if request.method == "POST":
        question_text = request.POST.get('question')

        if question_text and question_text.strip():
            question.question_text = question_text
            question.save()
            messages.success(request, "Question updated successfully!")

        return redirect('pollapp:edit_question', question_id=question.id)

    return render(request, 'pollapp/edit_question.html', {'question': question})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # 🔐 permission check
    if request.user != question.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete this question.")
        return redirect('pollapp:index')

    if request.method == "POST":
        question.delete()
        messages.success(request, "Question deleted successfully!")
        return redirect('pollapp:index')

    # ✅ IMPORTANT fallback return
    return redirect('pollapp:detail', question_id=question.id)

@login_required
def edit_choice(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)

    if request.user != choice.question.user and not request.user.is_superuser:
        return redirect('pollapp:index')

    if request.method == "POST":
        text = request.POST.get('choice_text')

        if text:
            choice.choice_text = text
            choice.save()
            return redirect('pollapp:detail', question_id=choice.question.id)

    return render(request, 'pollapp/edit_choice.html', {'choice': choice})

@login_required
def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    question_id = choice.question.id

    if request.user != choice.question.user and not request.user.is_superuser:
        return redirect('pollapp:index')

    if request.method == "POST":
        choice.delete()
        return redirect('pollapp:detail', question_id=question_id)

    return render(request, 'pollapp/delete_choice.html', {'choice': choice})

from django.contrib.auth.decorators import login_required

@login_required
def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # ✅ सही permission check
    if request.user != question.user and not request.user.is_superuser:
        return redirect('pollapp:index')

    if request.method == "POST":
        choice_text = request.POST.get('choice_text')

        if choice_text and choice_text.strip():
            Choice.objects.create(
                question=question,
                choice_text=choice_text
            )
            return redirect('pollapp:detail', question_id=question.id)

    return render(request, 'pollapp/add_choice.html', {'question': question})