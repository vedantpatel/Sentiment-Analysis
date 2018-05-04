import sys
import json
import time
import re
import tweepy
from tweepy import OAuthHandler   
from tweepy import Stream 
from tweepy import StreamListener
from textblob import TextBlob
import matplotlib.pyplot as plt    # For graphing 

# # To only get the unicode 
# "# -- coding: utf-8 --"

# Authentication Key from Twitter's Developer's Account
consumer_key= 'Consumer Key from Twitter'
consumer_secret= 'Secret key from Twitter'
access_token= 'Access Token from Twitter'
access_token_secret= 'Access Token Secret from Twitter'


auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

# Defining variables 
pos = 0
neg = 0 
neutral = 0
count = 0				# Counter for the tweet
timei = time.time()  			# To calculate 
plt.ion()				# Mode to set interactive graph 
 

# Listing to incoming Streams from tweepy Documentation
class listener(StreamListener):
    
    def on_data(self,data):
    	# Defining all the global variables 
        global timei
        global pos
        global neg     
        global neutral  
        global count

        data = json.loads(data)     		# Loading the data 
        tweet = data["text"].strip() 		# Parsing the text
        #username=data["user"]["screen_name"]
        #print("Username", username)
        timeint = int(time.time() - timei)
        tweet = " ".join(re.findall("[a-zA-Z]+", tweet))	# We want filter just the Alphabet and nothing else 
        tBlob = TextBlob(tweet.strip())  		        # Striping to get rid of unwanted characters from TextBlob

        # Setting count and sentence count 
        count = count + 1
        senticount = 0	

        # Iterating through all the sentences and adding it to senticount variable 	
        for sentence in tBlob.sentences:
            
            senticount = senticount + sentence.sentiment.polarity
            if sentence.sentiment.polarity >= 0:						# Positive
                pos = pos + sentence.sentiment.polarity   
            else:														# Negative
                neg = neg + sentence.sentiment.polarity  
        neutral = neutral + senticount        							# Neutral

        # Priniting all the data 
        print('Count:', count)
        print('Tweet: ' + tweet.strip())
        print('Sentence Count:', senticount)
        #print('Time:', timeint)
        print("Positive: " + str(pos) + ' ' + "Negative: " + str(neg) + ' ' + "Neutral: " + str(neutral))
        print('\n')
    
    	# Using Matplot lib to graph the sentiments 
        plt.axis([0, 70, -35,35])
        plt.title('Sentiments Analysis on Tweets (Search Topic: Apple)')
        plt.xlabel('Time')
        plt.ylabel('Sentiment')	
        plt.plot([timeint],[pos],'go',[timeint],[neg],'ro', [timeint],[neutral],'bo')
        #plt.legend(loc='best')

        plt.show()
        plt.pause(0.0001)   		# To show an animation 
        plt.savefig('foo.png')

        if count == 100:    		# Getting max upto 100 tweets at a time
            return False
        else:
            return True

# Input from Command Line 
search = input("Please enter your search: ")
if(len(search) == 0):
	print("Error: No input was provided")

# Getting authentication
tStream=  Stream(auth, listener(count))
# Will filter the inputted search from user 
tStream.filter(track=[search])

'''
    For Subplotting the graph 

    plt.subplot(311)
    plt.plot([timeint],[pos], color= 'green' , marker='o', label = 'Positive')
    plt.title('Sentiments Analysis on Tweet')
    plt.ylabel('Sentiment')
    #plt.legend(loc='best')
    
    plt.subplot(312)
    plt.plot([timeint],[neg], color= 'red' , marker='o', label = 'Negative')
    plt.ylabel('Sentiment')
    #plt.legend(loc='best')

    plt.subplot(313)
    plt.plot([timeint],[neutral], color= 'blue' , marker='o', label = 'Neutral')
    plt.xlabel('Time (sec)')
    plt.ylabel('Sentiment')
    #plt.legend(loc='best')
'''
