from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('<h1>Graph for Transactions</h1>')
def transactiongraoh(request,transaction_hsh):
    return HttpResponse("<h2>Graph for transaction: "+transaction_hsh+"</h2>")