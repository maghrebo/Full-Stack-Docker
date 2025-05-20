from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os 

app = Flask(__name__)
CORS(app)

@app.route('/')
def ping_server():
    return "Welcome to the world of animals."

@app.route('/simple_json')
def simple_json():
    return jsonify('{saluto:ciao}')

#Creo una funzione che posso riciclare ogni volta che devo accedere al DB
def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["animal_db"]
    return db

#Creo una route per ottenere tutti gli animali
@app.route('/animals')
def get_stored_animals():
    db=""
    try:
        db = get_db()
        _animals = db.animal_tb.find()
        animals = [{"id": animal["id"], "name": animal["name"], "type": animal["type"]} for animal in _animals]
        return jsonify({"animals": animals})
    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()

#Verifico di poter leggere le variabili d'ambiente impostate nel file docker-compose.yml
@app.route('/environment')
def env():
    return jsonify(
            {"env":[
                {"MONGO_INITDB_DATABASE": os.environ["MONGO_INITDB_DATABASE"]},
                {"MONGO_INITDB_ROOT_USERNAME": os.environ["MONGO_INITDB_ROOT_USERNAME"]},
                {"MONGO_INITDB_ROOT_PASSWORD": os.environ["MONGO_INITDB_ROOT_PASSWORD"]}
            ]})

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
