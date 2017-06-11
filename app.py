from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.charts import Line
from bokeh.embed import file_html,components
from bokeh.resources import CDN

app = Flask(__name__)

app.selection = {}
app.selection['api_key'] = 'CFzxVnJ2KGbz3yvxuLxz'

def generate_graph():
  url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?'
  r = requests.get(url,app.selection)
  rjson = r.json()['datatable']
  data = pd.DataFrame(rjson['data'])
  cols = pd.DataFrame(rjson['columns'])['name']
  data.columns = cols
  
  def convert_to_datetime(val):
    y, m, d = val.split('-')
    return pd.datetime(int(y),int(m),int(d))
  
  data['date'] = data['date'].apply(convert_to_datetime)
  data = data.set_index(['date'])
  
  t = 'Time series data for ' + app.selection['ticker']
  p = Line(data, title=t, xlabel='date', ylabel='price ($)')
  app.s, app.d = components(p)
  
  
#  html = file_html(p,CDN,'Data sourced from Quandl WIKI dataset')
#  f = open('templates/graph.html','w')
#  f.write(html)
#  f.close()
  return

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    app.selection['ticker']=request.form['ticker_symbol']
    app.selection['qopts.columns']='date,' + request.form['metric']
    generate_graph()
    return redirect('/graph')

@app.route('/graph', methods=['GET'])
def graph():
  return render_template('graph.html',script=app.s,div=app.d)

if __name__ == '__main__':
  app.run(port=33507)



