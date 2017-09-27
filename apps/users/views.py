from django.shortcuts import render, redirect
from django.contrib import messages
from sets import Set
from .models import User, Quote

# Create your views here.
def indexredirect(request):
    return redirect('/main')

def main(request):
    if 'id' in request.session:
        return redirect('/quotes')
    return render(request, 'users/index.html')

def quotes(request):
    if 'id' not in request.session:
        messages.error(request, ('Please register or login!'))
        return redirect('/main')
    id = request.session['id']
    user = User.objects.get(id=id)
    allquotes = Quote.objects.exclude(user_favorited=user)
    favequotes = Quote.objects.filter(user_favorited=user)
    return render(request, 'users/quotes.html', {'user': user, 'all': allquotes, 'fave': favequotes})

def register(request):
    results = User.objects.basic_validator(request.POST)
    if results[0]:
        request.session['id'] = results[1].id
        print request.session['id']
        return redirect('/quotes')
    else:
        for tag, error in results[1].iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')

def login(request):
    results = User.objects.login_validator(request.POST)
    if results[0]:
        request.session['id'] = results[1].id
        return redirect('/quotes')
    else:
        for tag, error in results[1].iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')

def process(request):
    errors = Quote.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/quotes')
    else:
        id = request.session['id']
        user = User.objects.get(id=id)
        quote = Quote(author=request.POST['author'], message=request.POST['message'])
        quote.poster = user
        quote.save()
        return redirect('/quotes')

def user(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        messages.error(request, ('User does not exist!'))
        return redirect('/quotes')
    quotes = Quote.objects.filter(poster=user)
    return render(request, 'users/user.html', {'user':user, 'quotes':quotes})

def join(request, id):
    quote = Quote.objects.get(id=id)
    u_id = request.session['id']
    user = User.objects.get(id=u_id)
    quote.user_favorited.add(user)
    return redirect('/quotes')

def remove(request, id):
    quote = Quote.objects.get(id=id)
    u_id = request.session['id']
    user = User.objects.get(id=u_id)
    quote.user_favorited.remove(user)
    return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/main')