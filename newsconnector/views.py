from django.shortcuts import render,  redirect
from django.core.urlresolvers import reverse
from newsconnector.models import *
from django.db.models import Min
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from datetime import date, timedelta, datetime

@login_required
def delete_keyword(request, pk):
    if(request.user.is_staff):
        keyword = get_object_or_404(Keyword, pk=pk)
        keyword.delete()
        
        redirect_url = request.GET.get('next', reverse('index'))
        return redirect(redirect_url)
    return redirect(reverse('index'))

def news(request):    
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday if datetime.now().hour < 13 else date.today()
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': NewsFeed.objects.all(),
                                          'title': 'LATEST NEWS',
                                          'latest': NewsArticle.objects.all().order_by('-date')[:10]})

def sports(request):    
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': SportsFeed.objects.all(),
                                          'title': 'LATEST SPORTS NEWS',
                                          'latest': SportsArticle.objects.all().order_by('-date')[:10]})

def finance(request):    
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday if datetime.now().hour < 13 else date.today()
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': FinanceFeed.objects.all(),
                                          'title': 'LATEST FINANCIAL NEWS',
                                          'latest': FinanceArticle.objects.all().order_by('-date')[:10]})

def entertainment(request):    
    #min_date = (Article.objects.aggregate(date = Min('date'))['date']).date()
    min_date = date.today() - timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)
    default_min_date = yesterday if datetime.now().hour < 13 else date.today()
    
    return render(request, 'index.html', {'min_date': min_date,
                                          'default_min_date': default_min_date,
                                          'sites': EntertainmentFeed.objects.all(),
                                          'title': 'LATEST GOSSIP',
                                          'latest': EntertainmentArticle.objects.all().order_by('-date')[:10]})
