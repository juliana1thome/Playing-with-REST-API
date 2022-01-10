import requests
import json

response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')

for question in response.json()['items']:
    if question['answer_count'] != 0:
        print("Question: " + question['title'])
        print("Link for the question " + question['link'])
        print("How many answers this question had " + str(question['answer_count']))
    else:
        print("No answer. So, let's skip this question")
