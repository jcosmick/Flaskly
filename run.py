from flask import Flask, flash, request, redirect, session, render_template
import os
from werkzeug.utils import secure_filename
from forms import CreaGraph1, CreaGraph2
import pandas as pd
import json
from utility_functions import *
from graph_functions import *
import plotly
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = get_random_string(20)
app.config['UPLOAD_FODLER'] = UPLOAD_FOLDER

@app.route("/home")
def home():
    titles = []
    for fileName in os.listdir(USER_DATA):
        if fileName.endswith(".json"):
            fileName = '/'+fileName
            file = open(USER_DATA + fileName)
            titles.append(json.load(file)["title"])
    titles.sort()
    return render_template('home.html', titles= titles)

@app.route("/c1", methods=['GET', 'POST'])
def creation_part1():
    form = CreaGraph1()

    if request.method == 'POST' and form.validate_on_submit():
        file = form.data_file.data
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            session['messages'] = filename
            return redirect('c2')
        flash("File non supportato", "error")

    return render_template("crea_parte1.html", form = form)

@app.route('/c2', methods=["GET", "POST"])
def creation_part2():
    form = CreaGraph2()

    filename = session['messages']
    df = pd.read_csv(UPLOAD_FOLDER+"/"+filename)
    colonne = df.columns.to_list()

    form_choices = []
    for colonna in colonne:
        form_choices.append((colonna,colonna))
    form.cols.choices = form_choices
    form.asseX.choices = form_choices
    form.asseY1.choices = form_choices
    form.asseY2.choices = form_choices

    if request.method == 'POST' and form.validate_on_submit():
        asseY2Data = "None"
        if form.asseY2.data != "None":
            asseY2Data = df[form.asseY2.data].to_list()

        data_to_write = {"title": form.title.data,
                        "columns": form.cols.data,
                        "asseX": form.asseX.data,
                        "asseXData": df[form.asseX.data].to_list(),
                        "asseY1": form.asseY1.data,
                        "asseY1Data": df[form.asseY1.data].to_list(),
                        "asseY2": form.asseY2.data,
                        "asseY2Data": asseY2Data
                        }
                #USER_DATA+"/"+session["username"]+"_"+get_random_string(4)+".json"
        with open(USER_DATA+"/"+get_random_string(4)+".json", "w") as outfile:
            json.dump(data_to_write, outfile)
        return redirect("/home")
    form.y2.data = None
    return render_template('crea_parte2.html', form = form, col = colonne)

@app.route('/v', methods=["GET", "POST"])
def visualizza_grafico():

    df = None
    for fileName in os.listdir(USER_DATA):
        if fileName == "wnac.json":
            fileName = '/'+fileName
            file = open(USER_DATA + fileName)
            jsonData = json.load(file)
            df = pd.DataFrame(jsonData["asseXData"], jsonData["asseY1Data"])

    graphJSON = json.dumps(plot_graf_2y(df[0],
                                        "Giorno",
                                        [df.index],
                                        ["Scatter"],
                                        ["pioggia"],
                                        "Pioggia",
                                        "Titolone",
                                        [False]),
                            cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('visualizza.html', graphJSON = graphJSON)

if __name__=='__main__':
   app.run()