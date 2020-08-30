# import necessary libraries
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
    
import pymysql
from config import remote_db_endpoint, remote_db_port
from config import remote_db_name, remote_db_user, remote_db_pwd
pymysql.install_as_MySQLdb()
from sqlalchemy import func, create_engine

app = Flask(__name__)

engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")

# create route that renders index.html template
@app.route("/")
def home():    
    return render_template("index.html")

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    conn = engine.connect()

    if request.method == "POST":
        Username = request.form["Username"]
        age = request.form["Age"]
        city = request.form["City"]
        state = request.form["State"]
        gender = request.form["Gender"]
        Discovery = request.form["Discovery"]

        game_df = pd.DataFrame({
            'Username': [Username],
            'Age': [age],
            'City': [city],
            'State': [state],
            'Gender': [gender],
            'Discovery': [Discovery]
        })

        game_df.to_sql('game', con=conn, if_exists='append', index=False)

        return redirect("/", code=302)

    conn.close()

    return render_template("RegisterForm.html")

@app.route("/info")
def info():
    conn = engine.connect()
    
    query = '''
        SELECT 
            *
        FROM
            game
    ''' 

    game_df = pd.read_sql(query, con=conn)

    game_json = game_df.to_json(orient='records')

    conn.close()

    return game_json

@app.route("/api/pals")
def pals():
    conn = engine.connect()
    
    query = '''
        SELECT 
            *
        FROM
            pets
    ''' 

    pets_df = pd.read_sql(query, con=conn)

    pets_json = pets_df.to_json(orient='records')

    conn.close()

    return pets_json

if __name__ == "__main__":
    app.run(debug=True)