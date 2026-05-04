from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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
            question = Question.objects.create(question_text=question_text)

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