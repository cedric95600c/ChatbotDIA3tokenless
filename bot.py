##########librairie#########
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
import re
import pandas as pd
import numpy as np
import os
import discord
nltk.download('wordnet')


GUILD= "SongRecommender"

client = discord.Client()
variable = 5

########panda############
data = pd.read_csv('data.csv', ',')
data = data.sort_values(by='Popularity',ascending=False)

list_genre = []
for i in data['Top Genre']:
  genre = i.split()
  for subgenre in genre:
    if subgenre not in list_genre and len(subgenre)>3:
      list_genre.append(subgenre)

list_year = data['Year'].unique()
list_artist = data['Artist'].unique()
list_title = data['Title'].unique()


def find_song(data,year,genre,artist):
  subset = data
  if year != 0:
    subset = subset[subset['Year']== year]
  if genre != "":
    subset = subset[subset['Top Genre'].str.contains(genre)]
  if artist != "":
    subset = subset[subset['Artist']== artist]
  return subset['Title'].iloc[0:5]

def match(message):
  genre=""
  artist=""
  year=0
  for i in list_genre:
    if i.lower() in message.lower():
      genre = i
  for j in list_year:
    if str(j) in message:
      year = j
  for k in list_artist:
    if k.lower() in message.lower():
      artist = k
  return genre,artist,year


###########fin panda#############
list_words=['hello','goodbye','recommend','play','help','yes']
list_syn={}
for word in list_words:
    synonyms=[]
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            
            # Remove any special characters from synonym strings
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
   
    list_syn[word]=set(synonyms)
    

# Building dictionary of Intents & Keywords
keywords={}
keywords_dict={}

# Defining a new key in the keywords dictionary
keywords['greet']=[]
keywords['recommend']=[]
keywords['goodbye']=[]
keywords['play']=[]
keywords['help']=[]
keywords['yes']=[]



# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['hello']):
    keywords['greet'].append('.*\\b'+synonym+'\\b.*')

for synonym in list(list_syn['goodbye']):
    keywords['goodbye'].append('.*\\b'+synonym+'\\b.*')

for synonym in list(list_syn['play']):
    keywords['play'].append('.*\\b'+synonym+'\\b.*')

for synonym in list(list_syn['help']):
    keywords['help'].append('.*\\b'+synonym+'\\b.*')
    

for synonym in list(list_syn['yes']):
    keywords['yes'].append('.*\\b'+synonym+'\\b.*')


for synonym in list(list_syn['recommend']):
    keywords['recommend'].append('.*\\b'+synonym+'\\b.*')




 

for intent, keys in keywords.items():
    
    # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
    keywords_dict[intent]=re.compile('|'.join(keys))

# Building a dictionary of responses
responses={
    'greet':'Hello! Do you want some information?',
    'goodbye':'Goodbye!',
    'recommend':' i will recommend you some song ',
    'play':'ok je joue le son:',
    'help':'this chatbot can recommand songs according to  artist genre and year. (use  recommend verb or his synonymes in english)',
    'yes':'this chatbot can recommand songs according to  artist genre and year. (use  recommend verb or his synonymes in english)',
    'fallback':'I dont understand. Could you repeat ',
}


# While loop to run the chatbot indefinetely
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    
@client.event
async def on_message(message):
    response = ""
    if message.author == client.user:
        return
    # Takes the user input and converts all characters to lowercase
     
     # Defining the Chatbot's exit condition
  
    
    matched_intent = None 
    for intent,pattern in keywords_dict.items():
        if re.search(pattern,message.content.lower()): 
            matched_intent=intent  
   
    # The fallback intent is selected by default
    key='fallback' 
    
    if matched_intent in responses:
       
        # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
        key = matched_intent 
    if key == "greet" or key == "help" or key == "goodbye"or key=='fallback'or key=='yes':
       response = responses[key]
    if key == 'fallback':
        if "music." in message.content.lower():
            response = ""
    if key == "recommend":
      genre,artist,year = match(message.content)
      result = find_song(data,year,genre,artist)
      list_recommendation=[]
      for i in result:
        a=''
        b=''
        c=''
        list_recommendation.append(i)
        if year!= 0:
          a = "a song from " + str(year) + " "
        if genre!= "":
          b = ' genre: ' + genre + " "
        if artist!="":
          c= 'artist: ' + artist + " "
 
        response = response + "\n" + a+b+c+i
      if list_recommendation == []:
        response = "no result found"
     
    if key == "play":
      for l in list_title:
        if l.lower() in message.content.lower():
          response = "if you want to play this song type precisely: \n"  
          response = response + "music.play " + l
      if response == "":
          response = "musique non reconnue"
      if "music." in message.content.lower():
            response = ""
        
    
    await message.channel.send(response)
    response = ""
   
    
client.run(TOKEN)


    