from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from poll.models import Poll_Vote, Poll_Choice, Poll
from django.contrib.auth.models import User
from datetime import datetime
from dateutil.parser import parse



# Create your views here.
@login_required
def index(request):
    context = {}
    poll_av = Poll.objects.filter(start_date__lte=datetime.now(),end_date__gte=datetime.now()).order_by('-start_date')
    poll_cl = Poll.objects.filter(start_date__lte=datetime.now(),end_date__lt=datetime.now()).order_by('-end_date')
    context['poll_av'] = poll_av
    context['poll_cl'] = poll_cl
    return render(request, 'poll/index.html', context=context)

@login_required
def poll_add(request):
    context = {}
    if request.method == 'POST':
        try:
            start_date = parse(request.POST.get('start_date'))
        except Exception:
            start_date = datetime.now()
        try:
            end_date = parse(request.POST.get('end_date'))
        except Exception:
            end_date = datetime.now()
        poll = Poll.objects.create(
            subject=request.POST.get('subject'),
            detail=request.POST.get('detail'),
            picture=request.FILES.get('picture'),
            start_date=start_date,
            end_date=end_date,
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
    if Poll.objects.filter(id=poll_id, start_date__lte=datetime.now(), end_date__gte=datetime.now()):
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
            if request.FILES.get('picture'):
                poll.picture = request.FILES.get('picture')
            try:
                poll.start_date = parse(request.POST.get('start_date'))
            except Exception:
                poll.start_date = datetime.now()
            try:
                poll.end_date = parse(request.POST.get('end_date'))
            except Exception:
                poll.end_date = datetime.now()
            poll.password = request.POST.get('password')
            poll.save()


        context['poll'] = poll
        context['choice'] = choice
        return render(request, 'poll/edit_poll.html', context=context)
    else:
        return redirect('login_user')
        
    

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
            if request.FILES.get("%d_image"%choice_item.id):
                choice_item.image = request.FILES.get("%d_image"%choice_item.id)
            choice_item.save()
            
    return redirect('/poll/edit/%s/'%poll_id)