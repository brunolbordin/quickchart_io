import requests as R
import datetime as dt
import csv
from PIL import Image
from IPython.display import display
from urllib.parse import quote


def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                "label": labels[i],
                "data": y[i]
            })
        return datasets
    else:
        return [
            {
                "label": labels[0],
                "data": y
            }
        ]


def set_title(title=""):
    if title != "":
        display = "true"
    else:
        display = "false"
    return {
        "title": {
            "display": display,
            "text": title
        }
    }


def create_chart(x, y, labels, kind="bar", title=""):
    datasets = get_datasets(y, labels)
    options = set_title(title)

    chart = {
        "type": kind,
        "data": {
            "labels": x,
            "datasets": datasets,
        },
        "options": options
    }

    return chart


def get_api_chart(chart):
    url_base = "https://quickchart.io/chart"
    resp = R.get(f"{url_base}?c={str(chart)}")
    return resp.content


def save_image(path, content):
    with open(path, "wb") as image:
        image.write(content)


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


def get_api_qrcode(link):
    text = quote(link) # parsing link to url
    url_base = "https://quickchart.io/qr"
    resp = R.get(f"{url_base}?text={text}")
    return resp.content

url = "https://api.covid19api.com/dayone/country/brazil"

resp = R.get(url)

raw_data = resp.json()

final_data = []

for obs in raw_data:
    final_data.append([obs["Confirmed"], obs["Deaths"], obs["Recovered"], obs["Active"], obs["Date"]])

final_data.insert(0, ["Confirmados", "Obitos", "Recuperados", "Ativos", "Data"])

CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]

with open("brasil-covid.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(final_data)

for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], "%Y-%m-%d")

y_data_1 = []
for obs in final_data[1::150]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in final_data[1::150]:
    y_data_2.append(obs[RECUPERADOS])

labels = ["Confirmados", "Recuperados"]

x = []
for obs in final_data[1::150]:
    x.append(obs[DATA].strftime("%d/%m/%Y"))

chart = create_chart(x, [y_data_1, y_data_2], labels, title="Gráfico CONFIRMADOS vs RECUPERADOS")
chart_content = get_api_chart(chart)
save_image("First_Graphic.png", chart_content)

url_base = "https://quickchart.io/chart"
link = f"{url_base}?c={str(chart)}"
save_image("qr-code.png", get_api_qrcode(link))

