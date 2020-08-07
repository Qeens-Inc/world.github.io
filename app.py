from flask import Flask, render_template, request, jsonify, session
import json
import requests
import time

app=Flask(__name__)
locations=["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
                "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
                "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
                "Burkina Faso", "Burma", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
                "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Brazzaville)", "Congo (Kinshasa)", "Costa Rica", "Cote d\"Ivoire",
                "Croatia", "Cuba", "Cyprus", "Czechia", "Denmark", "Diamond Princess", "Djibouti", "Dominica", "Dominican Republic", 
                "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France",
                "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
                "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan",
                "Jordan", "Kazakhstan", "Kenya", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", 
                "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "MS Zaandam", "Madagascar", "Malawi", "Malaysia",
                "Maldives", "Mali", "Malta", "Mauritania", "Mauritius", "Mexico", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
                "Namibia", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Panama",
                "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
                "Saint Vincent and the Grenadines", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles",
                "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
                "Sweden", "Switzerland", "Syria", "Taiwan*", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Trinidad and Tobago", "Tunisia", "Turkey",
                "US", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "Uruguay", "Uzbekistan", "Venezuela", "Vietnam", "West Bank and Gaza",
                "Western Sahara", "Yemen", "Zambia", "Zimbabwe"]

apis=[{'name':'Total','url':'api/total','data':'Returns all total cases in the world'},
                    {'name':'Current','url':'api/cases','data':'Returns all cases per country'},
                    {'name':'Country','url':'api/{country name}','data':'Returns Specific country'},
                    {'name':'Countries','url':'api/countries','data':'Returns list of all countries affected'}]

data=[]

@app.route('/')
def home():
  return render_template('home.html',home='active')
  

@app.route('/about')
def about():
  return render_template('about.html',about='active')
  

@app.route('/countries/')
def countries():
  try:
    request=requests.get('https://covid2019-api.herokuapp.com/v2/current')
  except requests.exceptions.RequestException:
    return render_template('error.html',val=404)
  if not request.status_code==200:
    return render_template('error.html',val=request.status_code)
  else: 
    data=json.loads(request.text)['data']
    datas=[]
    for location in locations:
      for d in data:
        if d['location']==location:
          datas.append(d)
          del(d)
          break
    return render_template('countries.html',countries='active',datas=datas)


@app.route('/api')
def api():
  return render_template('api.html',api='active',apis=apis)

@app.route('/api/total')
def total():
  return req('v2/total')

@app.route('/api/countries')
def _countries():
  return req('countries')

@app.route('/api/cases')
def cases():
  return req('v2/current')

@app.route('/api/<string:country>')
def _country(country):
  if country[0].upper()+country[1:].lower() in locations:
    return req(f'v2/country/{country.lower()}')
  else:
    return jsonify({'Error':'No such country'})



def req(url):
  try:
    request=requests.get('https://covid2019-api.herokuapp.com/'+url)
  except requests.exceptions.RequestException:
    return jsonify({'stat':"Error"})
  if request.status_code==200:
    return request.text
  else:
    return jsonify({'stat':"Error"})



if __name__=='__main__':
  app.run(debug=True,port=4000)