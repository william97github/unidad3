import requests as requests
from flask import Flask, render_template
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost"
client = MongoClient(MONGO_URI)
db = client['RickMorty']
collection = db['personajes']

for pagina in range(1, 22):
    peticion = requests.get(f"https://rickandmortyapi.com/api/character?page={pagina}")
    datos = peticion.json()
    collection.insert_many(datos["results"])

app = Flask(__name__)

@app.route("/")
def examen():
    todos = collection.aggregate([{ "$sort" : { "id" : -1 } }])
    return render_template("index.html", lista = todos)

@app.route("/ver/<int:codigo>")
def perfil(codigo):
    perf = collection.find({ "id": codigo })
    return render_template("perfil.html", perfil = perf)

@app.route("/capitulo/<int:capitulo>")
def capitulo(capitulo):
    perf = collection.find({"episode":{"$all":[f'https://rickandmortyapi.com/api/episode/{capitulo}']}})
    return render_template("capitulo.html", capitulo=perf)
