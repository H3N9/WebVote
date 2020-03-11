from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from poll.models import Poll_Vote, Poll_Choice, Poll
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.
@login_required
def index(request):
    context = {}
    context['poll_av'] = Poll.objects.filter(start_date__lte=datetime.now(),end_date__gte=datetime.now())
    context['poll_cl'] = Poll.objects.exclude(start_date__lte=datetime.now(),end_date__gte=datetime.now())
    return render(request, 'poll/index.html', context=context)

@login_required
def poll_add(request):
    context = {}
    if request.method == 'POST':
        poll = Poll.objects.create(
            subject=request.POST.get('subject'),
            detail=request.POST.get('detail'),
            picture=request.FILES.get('picture'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            password=request.POST.get('password'),
            create_by_id=request.user.id)
        return redirect('mine')
    else:
        poll = Poll.objects.none()
    context['poll'] = poll
    return render(request, 'poll/poll_add.html', context=context)

@login_required
def detail(request, poll_id):
    context = {}
    ever = 1
    end = 0
    poll = Poll.objects.get(pk=poll_id)
    choice = Poll_Choice.objects.filter(poll_id_id=poll_id)
    vote = Poll_Vote.objects.filter(poll_id_id=poll_id,vote_by_id=request.user.id)
    vote_all = Poll_Vote.objects.filter(poll_id_id=poll_id)
    votes = []
    percent_user = 0
    key = 0
    if poll.password and request.POST.get("password") != poll.password:
        key =  1
    else:
        key = 0
    if vote_all:
        for vote_choice in choice:
            percent_user = round(Poll_Vote.objects.filter(poll_id_id=poll_id,choice_id_id=vote_choice.id).count()/vote_all.count()*100)
            among = Poll_Vote.objects.filter(poll_id_id=poll_id, choice_id_id=vote_choice.id).count()
            votes.append([vote_choice.subject, among, percent_user])
    if vote:
        vote = Poll_Vote.objects.get(pk=vote[0].id)
        ever = 0
    else:
        vote = Poll_Vote.objects.none()
    if Poll.objects.filter(id=poll_id, end_date__gte=datetime.now()):
        end = 1
    context['key'] = key
    context['password'] = request.POST.get("password")
    context['end'] = end
    context['ever'] = ever
    context['poll'] = poll
    context['choice'] = choice
    context['vote'] = vote
    context['vote_choice'] = votes
    context['password'] = poll.password
    return render(request, 'poll/detail.html', context=context)

@login_required
def mine(request):
    context = {}
    poll = Poll.objects.filter(create_by_id=request.user.id)
    context['poll'] = poll
    context['user'] = request.user.username
    return render(request, 'poll/my_poll.html', context=context)

@login_required
def edit(request, poll_id):

    if request.user.id == Poll.objects.get(pk=poll_id).create_by_id:
        context = {}
        poll = Poll.objects.get(pk=poll_id)
        choice = Poll_Choice.objects.filter(poll_id_id=poll_id)
        if request.method == 'POST':

            poll.subject = request.POST.get('subject')
            poll.detail = request.POST.get('detail')
            poll.picture = request.FILES.get('picture')
            poll.start_date = request.POST.get('start_date')
            poll.end_date = request.POST.get('end_date')
            poll.password = request.POST.get('password')
            poll.save()


        context['poll'] = poll
        context['choice'] = choice
    else:
        return redirect('login_user')  
    return render(request, 'poll/edit_poll.html', context=context)

@login_required
def choice_add(request, poll_id):
    if request.method == 'POST':
        choice = Poll_Choice.objects.create(
            subject=request.POST.get('choice_subject'),
            image=request.FILES.get('choice_image'),
            poll_id_id=poll_id,
        )
    return redirect('/poll/edit/%s/'%poll_id)

@login_required
def choice_delete(request, poll_id,choice_id):
    if request.user.id == Poll.objects.get(pk=poll_id).create_by_id:
        choice = Poll_Choice.objects.get(pk=choice_id)
        choice.delete()
    else:
        return redirect('login_user')
    return redirect('/poll/edit/%s/'%poll_id)

@login_required
def vote(request, poll_id):
    if request.method == 'POST':
        vote = Poll_Vote.objects.create(
            poll_id_id=poll_id,
            choice_id_id=request.POST.get('choose'),
            vote_by_id=request.user.id,
        )
    return redirect('/poll/detail/%s/'%poll_id)

@login_required
def poll_delete(request, poll_id):
    if request.user.id == Poll.objects.get(pk=poll_id).create_by_id:
        poll = Poll.objects.get(pk=poll_id)
        poll.delete()
    else:
        return redirect('login_user')
    return redirect('mine')

@login_required
def choice_save(request, poll_id):
    if request.method == 'POST':
        choice = Poll_Choice.objects.filter(poll_id_id=poll_id)
        for choice_item in choice:
            choice_item.subject = request.POST.get("%d"%choice_item.id)
            choice_item.image = request.FILES.get("%d_image"%choice_item.id)
            choice_item.save()
            
    return redirect('/poll/edit/%s/'%poll_id)