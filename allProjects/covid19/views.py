from django.shortcuts import render, redirect
import requests 
from bs4 import BeautifulSoup
import os 
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from random import randint

# Create your views here.
# Get covid-19 Statewise Status
extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'
response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 
header = extract_contents(soup.tr.find_all('th')) 
activeCase = extract_contents(soup.section.find_all('ul')) 
stats = [] 
all_rows = soup.find_all('tr') 

for row in all_rows[1:]: 
	stat = extract_contents(row.find_all('td')) 
	if stat: 
		if len(stat) == 5: 
			# last row 
			stat = ['', *stat] 
			stats.append(stat)
		elif len(stat) == 4: 
			stats.append(stat) 

totalcase = stats[-1]
stats.remove(stats[-1]) 

data = stats
activeCase = activeCase[0][0:4]

def index(request):
	title = "Covid-19 | Statewise Status"
    
	return render(request, 'covid19/index.html', {'mydata':data, 'maxcase':totalcase, 'activeCase':activeCase, 'title':title})


# Symptom Checker

df = pd.read_csv('https://raw.githubusercontent.com/Pradeepsuthar/Pradeepsuthar.github.io/master/com.csv')

# Train test spliting
def split_data(data, ratio):
  np.random.seed(42)
  shuffled = np.random.permutation(len(data))
  test_set_size = int(len(data) * ratio)
  test_indices = shuffled[ :test_set_size]
  train_indices = shuffled[test_set_size: ]
  return data.iloc[train_indices], data.iloc[test_indices]


train, test = split_data(df, 0.2)

x_train = train[['fever','bodyPain','age','runnyNose','diffBreath']].to_numpy()
x_test = test[['fever','bodyPain','age','runnyNose','diffBreath']].to_numpy()

# y_train = train[['infectionProb']].to_numpy().reshape(1,-1)
# y_test = test[['infectionProb']].to_numpy().reshape(1,-1)

y_train = train[['infectionProb']].to_numpy().reshape(119,)
y_test = test[['infectionProb']].to_numpy().reshape(29,)

# print("Y-Train\n",x_train)
# print("Y-Test\n",y_test)
clf = LogisticRegression()
clf.fit(x_train, y_train)

def symptomChecker(request):
	title = "Covid-19 | Symptom Checker"
    
	return render(request, 'covid19/symptomChecker.html', {'title':title})

def symptomCheckerTool(request):
	title = "Covid-19 | Symptom Checker Tool"
	infect = ''
	risk = 0
	predict_age = 0
	predict_fever = 0
	predict_runnyNose = 0
	predict_diffBreath = 0
	predict_bodyPain = 0
    
	if request.method == 'POST':
		# feathers
		fever = request.POST['fever']
		bodyPain = request.POST['bodyPain']
		age = request.POST['age']
		gender = request.POST['gender']
		runnyNose = request.POST['runnyNose']
		diffBreath = request.POST['diffBreath']

		if age == 'Less than 12 years':
			predict_age = randint(1,12)
		elif age == '12 - 50 years':
			predict_age = randint(12,50)
		elif age == '51 - 60 years':
			predict_age = randint(51,60)
		else:
			predict_age = randint(60,100)

		if fever == 'Yes':
			predict_fever = 1
		else:
			predict_fever = 0

		if runnyNose == 'Yes':
			predict_runnyNose = 1
		else:
			predict_runnyNose = 0 

		if diffBreath == 'Yes':
			predict_diffBreath = 1
		else:
			predict_diffBreath = 0

		if bodyPain == 'Yes':
			predict_bodyPain = 1
		else:
			predict_bodyPain = 0


		print("Gender :",gender)
		print("Age :",age)
		print("Do you have fever :",fever)
		print("Do you have runny Nose  :",runnyNose)
		print("Do you have body pain :",bodyPain)
		print("Do you have difficutly to breath :",diffBreath)

		user_input = [predict_fever,predict_bodyPain,predict_age,predict_runnyNose,predict_diffBreath]

		infect_status = clf.predict([user_input])

		infect_prob = clf.predict_proba([user_input])

		infect_chance = round(infect_prob[0][1]*100)

		if infect_status:
			infect = 'Hight Risk'
			risk = 1
		else:
			infect = 'Low Risk'
			risk = 0

		# response_data = [ ['1. ',fever], ['4. Do you have fever? <br>',bodyPain], [3,gender], [4,age], [5,runnyNose], [6,diffBreath] ]

		response_data = {
			"What is your gender?":gender,
			"What is your age-group?":age,
			"Do you have fever?":fever,
			"Do you have Cold?":runnyNose,
			"Do you have body pain?":bodyPain,
			"Do you fill shortness of breath?":diffBreath,
			}
		


		return render(request, 'covid19/response.html', {'title':"Covid-19 | Response",'response_data':response_data,'risk':risk,'infect_prob':infect_chance})
		
	return render(request, 'covid19/sympCheckTool.html', {'title':title})


def symptomCheckerResponse(request):
	title = "Covid-19 | Response"

	return render(request, 'covid19/response.html', {'title':title})

def StatisticsMap(request):
	
	return render(request, 'covid19/Statistics/index.html')
	