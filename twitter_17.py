import os
import json
import requests
import sys
import tweepy
import numpy as np
import py2neo

# MATCH (p:Person {name:person['profile']['name']['formatted']}),
#       (t:Twitter {handle:twitter_data[0]})


def rel_Transaction2Block(transaction,blockhash,graph):
   # Build query
   query = """
   WITH {transaction} as transaction,{blockhash} as blockhash
   MATCH (tx:Transaction {hsh:transaction['txid']}),
         (b:Block {hash:blockhash})
   MERGE (tx)-[:PartOf]->(b)
   """
   # Send Cypher query.
   graph.run(query,transaction=transaction,blockhash=blockhash)
   return True

def add_Block2Graph(block,graph):
   # Build query
   query = """
   WITH {block} as q
   MERGE (b:Block {hash:q['hash'],size:q['size'],height:q['height'],version:q['version'],merkleroot:q['merkleroot'],nonce:q['nonce'],bits:q['bits'],difficulty:q['difficulty'],chainwork:q['chainwork'],confirmations:q['confirmations'],previousblockhash:q['previousblockhash'],nextblockhash:q['nextblockhash'],reward:q['reward'],isMainChain:q['isMainChain'],poolInfo:q['poolInfo']['poolName']})
   """
   # Send Cypher query.
   graph.run(query,block=block)
   return True


def rel_Followers2Twitter(twitter,followers,graph):
   # Build query
   query = """
   WITH {twitter} as twitter_data,{followers} as followers
   UNWIND followers as fol
   MATCH (t:Twitter {handle:fol[0]}),
         (f:Twitter {handle:twitter_data})
   MERGE (t)-[:Follows]->(f)
   """
   # Send Cypher query.
   graph.run(query,twitter=twitter,followers=followers)
   return True


def rel_Person2Twitter(person,twitter,graph):
   # Build query
   query = """
   WITH {twitter} as twitter_data,{person} as person
   MATCH (p:Person {name:person}),
         (t:Twitter {handle:twitter_data[0]})
   MERGE (p)-[:HASTwitterAccount]->(t)
   """
   # Send Cypher query.
   graph.run(query,person=person,twitter=twitter)
   return True


def add_Twitters2Graph(Twitters,graph):
   # Build query
   query = """
   WITH {twitters} as data
   UNWIND data as q
   MERGE (t:Twitter {handle:q[0],name:q[1]})
   """
   # Send Cypher query.
   graph.run(query,twitters=Twitters)
   return True


consumer_key        = 'LpACmv9AtbFEzas7CK6jpeYDF'
consumer_secret     = 'YQG1gCUfsoRWFao5Rh0H5dwxjdLP05rZgJ7RCxFsYBAQM5xx8z'
access_token        = '767334748247191552-EQ8SS8sI49EMV0jF02IdeQ1fhsxNGvL'
access_token_secret = 'orymGZ57CwdaER5pJxzAnfb82lvNNhbEYX41ALyLq1LYN'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

name = api.get_user( sys.argv[1] ).name

followers_list = []

followers_list.append( [sys.argv[1], name] )

for user in tweepy.Cursor(api.followers, sys.argv[1] ).items():
    # print(user.screen_name + ", " + user.name)
    followers_list.append( [user.screen_name, user.name] )

# print( np.matrix( followers_list ) )



#################################################################



# set up authentication parameters
py2neo.authenticate("46.101.180.63:7474", "neo4j", "uni-bonn")

# Connect to graph and add constraints.
neo4jUrl = os.environ.get('NEO4J_URL',"http://46.101.180.63:7474/db/data/")
graph = py2neo.Graph(neo4jUrl)



add_Twitters2Graph(followers_list,graph)

print("followers_list[0][1]: " + followers_list[0][1] + ", " + "followers_list[0][0]: " + followers_list[0][0] )

rel_Person2Twitter(followers_list[0][1],followers_list[0],graph)

person = followers_list[0][0]

followers_list.pop(0)

rel_Followers2Twitter(person,followers_list,graph)


