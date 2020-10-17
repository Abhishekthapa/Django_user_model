from django.shortcuts import render
from account.models import Account

# Create your views here.


def home_screen_view(request):
    # print(request.headers)
    # context is a dictionary
    context = {}
    # context['some_string'] = "it is what it  is"
    # line 8 and 9 can be done as
    # context ={
    #     'some_string' : 'it is what it is'
    # }
    # list of value is a list
    # list_of_values = []
    # list_of_values.append('first entry')
    # list_of_values.append('second entry')
    # list_of_values.append('third entry')
    # list_of_values.append('forth entry')
    # context['list'] = list_of_values
    users = Account.objects.all()
    context['list'] = users
    return render(request, 'personal/home.html', context)
