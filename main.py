import argparse
import datetime
import pandas
import collections

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_year_text(year=1920):
    let = ' лет'
    god = ' год'
    goda = ' года'

    now = datetime.datetime.now()
    number = now.year - year
    if number % 100 in range(11, 21):
        return f'{number}{let}'
    elif number % 10 == 1:
        return f'{number}{god}'
    elif number % 10 in range(2, 5):
        return f"{number}{goda}"
    else:
        return f"{number}{let}"


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    parser = argparse.ArgumentParser(description='Wine collection web app')
    parser.add_argument(
        '--excel', '-e',
        default='wine3.xlsx',
        help='Путь к Excel-файлу с данными о винах (по умолчанию wine3.xlsx)'
    )

    args = parser.parse_args()

    excel_data = pandas.read_excel(
        args.excel,
        na_values=['', 'nan', 'NaN', 'NULL', '#N/A', '#VALUE!', '#DIV/0!', '#REF!', '#NAME?', '#NUM!'],
        keep_default_na=False
    )
    excel_data = excel_data.fillna('')
    wines = excel_data.to_dict(orient='records')

    wines_by_category = collections.defaultdict(list)
    for wine in wines:
        wines_by_category[wine['Категория']].append(wine)

    rendered_page = template.render(
        year_logo=get_year_text(),
        wines_by_category=wines_by_category
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
