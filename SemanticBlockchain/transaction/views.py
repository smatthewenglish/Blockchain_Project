from django.shortcuts import render
from django.http.response import HttpResponse
import py2neo
import os
# Create your views here.


def index(request):
    return HttpResponse('<h1>Graph for Transactions</h1>')
def transactiongraoh(request,transaction_hsh):
    # return HttpResponse("<h2>Graph for 1 transaction: "+transaction_hsh+"</h2>")

    py2neo.authenticate("46.101.180.63:7474", "neo4j", "uni-bonn")
    neo4jUrl = os.environ.get('NEO4J_URL', "http://46.101.180.63:7474/db/data/")
    graph = py2neo.Graph(neo4jUrl)

    # get transaction node
    query = """
               MATCH (p:Transaction {hsh:{y}})
               return p
               """

    # get sender and reciver
    query2="""
            MAtch (p:Transaction {hsh:{y}}),(sender:BTC_Address), (receiver:BTC_Address)
            MATCH (sender)-[r:send]->(p)
            MATCH (p)-[rr:send]->(receiver)
            return p,sender,receiver, r,rr
    """
    # Send Cypher query.

    q1 = graph.run(query,y="2e9f40d4af66964a526d51233f87c401eaf66e05afd1e65928d2f2a51e636232")
    transaction_obj = None;
    # print(x)
    for rec in q1:
        transaction_obj = rec[0]

    q2 = graph.run(query2,y="2e9f40d4af66964a526d51233f87c401eaf66e05afd1e65928d2f2a51e636232")
    transaction_s = None;

    for rec2 in q2:
        print(rec2)
        transaction_s = rec2[0]



    return render(request, 'transaction.html', {
        'transaction_hash' : transaction_hsh,
        'transaction' : transaction_obj
    })
