from flask import Flask, redirect, url_for, request, render_template
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)
dataFile = open('test.json')
data = json.load(dataFile)

@app.route('/', methods = ['POST', 'GET'])
def index():
  if request.method == 'POST':
    request_data = request.get_json()
    print(request_data, flush=True)
    if request_data['queryResult']['intent']['displayName'] == 'Progressed Symptoms':
      result = get_result(request_data)
      dataFile.close()
      return json.dumps({"fulfillmentText": result})
    else:
      dataFile.close()
      custom_payload = request_data['queryResult']['fulfillmentMessages'][2]['payload']['custom']
      return json.dumps({"fulfillmentText": custom_payload})

def get_lifespanIndex(outputContexts):
  lifespanCountList = []
  for outputContext in outputContexts:
    if 'lifespanCount' in outputContext :
      lifespanCount = (outputContext['lifespanCount'])
      lifespanCountList.append(lifespanCount)
    lifespanCountList.sort()
    minLifeSpan = lifespanCountList[0]
    return lifespanCountList.index(minLifeSpan)

def get_result(request_data):
  outputContexts = request_data["queryResult"]["outputContexts"]
  lifespanIndex = get_lifespanIndex(outputContexts)
  parameters = outputContexts[lifespanIndex]['parameters']
  age = parameters['number']
  gender = parameters['gender']
  temperature = parameters['temperature']
  symptoms = parameters['symptoms']
  additionalSymptoms = parameters['additional-symptoms']
  travel = parameters['travel']
  historyConditions = parameters['history-conditions']
  progressedSymptoms = parameters['progressed-symptoms']
  score = get_score(gender,temperature,symptoms,additionalSymptoms,travel,historyConditions,progressedSymptoms)
  if (score <= 3.5):
    return "Good news! You have low risk to get infected by corona. You are for safe now but kindly be aware. Stay Clean, Stay healthy"
  elif (score >= 3.6) & (score <= 6.9):
    return "You have Medium risk to get infected by corona virus. Need to be careful. For help kindly contact 9976782872"
  else:
    return "Sorry to say. You have High risk to get infected by corona virus. Kindly contact 9976782872 please don't make any contact with any people." 

def get_score(gender,temperature,symptoms,additionalSymptoms,travel,historyConditions,progressedSymptoms):
  additonalSymptomScore = 0
  temperatureScore = 0
  genderScore = 0
  symptomScore = 0 
  travelScore = 0
  historyConditionsScore = 0
  progressedSymptomsScore = 0
  for genderCategory in data['temperature']['options']:
    if genderCategory['value'] in gender:
      genderScore = genderCategory['score']

  for temp in data['temperature']['options']:
    if temp['value'] in temperature:
      temperatureScore = temp['score']

  for symp in data['symptoms']['options']:
    if symptoms in symp['value']:
      symptomScore = symp['score']

  for addSymp in data['additional_symptoms']['options']:
    if additionalSymptoms in addSymp['value']:
      additonalSymptomScore = addSymp['score']

  for trvl in data['travel']['options']:
    if travel in trvl['value']:
      travelScore = trvl['score']

  for history in data['history_conditions']['options']:
    if historyConditions in history['value']:
      historyConditionsScore = history['score']

  for progSymptom in data['progressed_symptoms']['options']:
    if progressedSymptoms in progSymptom['value']:
      progressedSymptomsScore = progSymptom['score']

  score = temperatureScore + symptomScore + additonalSymptomScore + travelScore + historyConditionsScore + progressedSymptomsScore + genderScore
  return score

if __name__ == '__main__':
  app.run(debug=True)
