from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import pandas
import collections
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html','xml'])
)

template = env.get_template('template.html')

let = ' лет'
god = ' год'
goda = ' года'

now = datetime.datetime.now()
number = now.year - 1294
if number%100 in range(11,21):
    text = str(number) + let
elif number%10 == 1:
    text = str(number) + god
elif number%10 in range(2,5):
    text = str(number) + goda
else: text = str(number) + let

excel_data = pandas.read_excel('wine3.xlsx', na_values=['', 'nan', 'NaN', 'NULL', '#N/A', '#VALUE!', '#DIV/0!', '#REF!', '#NAME?', '#NUM!'], keep_default_na=False)

excel_data = excel_data.fillna('')
wines = excel_data.to_dict(orient='records')

# Группируем вина по категориям
wines_by_category = collections.defaultdict(list)
for wine in wines:
    wines_by_category[wine['Категория']].append(wine)

rendered_page = template.render(
    year_logo = text,
    wines_by_category = wines_by_category
)

with open('template.html','w',encoding='utf8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
