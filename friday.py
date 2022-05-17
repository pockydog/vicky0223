from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)  #建構式宣告 #代表的是當前模組的名稱，讓flask之後要在哪裡找資源
# app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False  #顯示正確中文時使用

tpe = {
    "id": 0,
    "city_name": "台北",
    "country_name": "台灣",
    "is_capital": True
}
nyc = {
    "id": 1,
    "city_name": "紐約",
    "country_name": "美國",
    "is_capital": False
}
ldn = {
    "id": 2,
    "city_name": "倫敦",
    "country_name": "英國",
    "is_capital": True
}
cities = [tpe, nyc, ldn]

gapminder = pd.read_csv('gapminder.csv')
gapminder_list = list()
nrows = gapminder.shape[0]
for i in range(nrows):
    ser = gapminder.loc[i, :]
    row_dict = {}
    for idx, val in zip(ser.index, ser.values):
        row_dict[idx] = val
    gapminder_list.append(row_dict)

@app.route('/cities/all', methods=['GET'])
def cities_all():
    return jsonify(cities)

@app.route('/gapminder/all', methods=['GET'])
def gapminder_all():
    return jsonify(gapminder_list)


app.run()
