from onename import OnenameClient
import tweepy
import sparql


#onename settings
onename_client      = OnenameClient("afabb003acbbbb894ad43eab2911d021","25537176673eb8d5095e2d3c1b51c4fd233f448277bf1dfee5acf5c9ff199381")
consumer_key        = "ux3VSJ6g8cpGcNy2RJY8bdhQx"
consumer_secret     = "F9K6goaFJ6McsruzHc0530YXiRZB00SWdWLgLoy8rkRQMx9ulI"
access_token        = "14387505-2Ni7oevp6y0X9aub1yaUCQRoS68S7FJ6xDQ5WxU68"
access_token_secret = "inDZBPNcKQyvTdAyjUwZnvxZClqVslWf7T3qPT1wyjp7c"

#twitter settings
auth                = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api                 = tweepy.API(auth)

#functions

def getTwitterUserFromOnenameUser(onename):

    accounts        = onename_client.get_users([onename])[onename]["profile"]["account"]
    for account in accounts:
        if account["service"] == "twitter":
            return api.get_user(account["identifier"]).id
            # return account["identifier"]




#end functions

#main

user_profile = onename_client.get_users(['fredwilson'])


user_profile2 = getTwitterUserFromOnenameUser("ernane")
print("birl '%s'" % (user_profile2))


rootUserAdress = user_profile['fredwilson']['profile']['bitcoin']['address']


# fake list of address
address1 = onename_client.get_users(['naval'])['naval']['profile']['bitcoin']['address']

# original list from function query from toshi sparql
# listOfAddress = getAllTransactionsFromAddress(rootUserAdress).getAddress()

listOfAddress = []
# listOfAddress.append(str(address1))
# listOfAddress.append("1QJQxDas5JhdiXhEbNS14iNjr8auFT96GP")
listOfAddress.append("135QsW71hce7PoHLK5iyBhmuaiMka75twt")


print(listOfAddress)
for address in listOfAddress:
	# https://api.onename.com/v1/addresses/{address}/names
	# receiverOnenameUsers = getUsersFromAddress(address)
    print(address)
    # Returns an array of the names that the address owns.
    listOfOneNames = onename_client.get_names(address)
# end for

# print(listOfNames["results"])

# twitter

# listOfOneNames are a list of user that got money from rootUser
# for  onenameUser in listOfOneNames:

    listFollowersFromRootUser =  api.followers_ids("ernane")
    print(listFollowersFromRootUser)
    # getTwitterUserFromOnenameUser(onenameUser)
    # twitterId = getTwitterUserFromOnenameUser(onenameUser)
    # print(twitterId)

    if 197497888 in listFollowersFromRootUser:
        print("foi")




# if twitterFriends.lenght > 0
# 	return twitterFriends
# else
# 	return "no friends"




q = ('SELECT DISTINCT ?station, ?orbits WHERE { '
      '?station a <http://dbpedia.org/ontology/SpaceStation> . '
      '?station <http://dbpedia.org/property/orbits> ?orbits . '
      'FILTER(?orbits > 50000) } ORDER BY DESC(?orbits)')
result = sparql.query('http://dbpedia.org/sparql', q)

print(result.variables)