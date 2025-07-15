import pandas
import collections
import pprint
import json

excel_data = pandas.read_excel('wine2.xlsx', na_values=['', 'nan', 'NaN', 'NULL', '#N/A', '#VALUE!', '#DIV/0!', '#REF!', '#NAME?', '#NUM!'], keep_default_na=False)
# Заменяем NaN на пустые строки
excel_data = excel_data.fillna('')


wines = excel_data.to_dict(orient='records')
print(wines)

wines_by_category = collections.defaultdict(list)
for wine in wines:
    wines_by_category[wine['Категория']].append(wine)

# Красивый вывод с pprint
pprint.pprint(dict(wines_by_category))

# for wine in wines:
#     print(wine)  # замените 'Название' на имя вашего столбца


