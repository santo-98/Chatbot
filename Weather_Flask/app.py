from flask import Flask, redirect, url_for, request, render_template
import requests
import json

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
  if request.method == 'GET':
    req = str(request.args.get('text'))
    data = json.dumps({"sender": "Rasa","message": req})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post('http://localhost:5005/webhooks/rest/webhook', data = data, headers = headers)
    res = res.json()
    res = res[0]['text']
    return res

if __name__ == '__main__':
  app.run(debug=True, port= 9001)