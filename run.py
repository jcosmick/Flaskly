from flask import Flask, flash, request, redirect, session, render_template
import os
from werkzeug.utils import secure_filename
from forms import  *
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
    grafs = []
    for fileName in os.listdir(USER_DATA):
        graf = {}
        if fileName.endswith(".json"):
            graf.update({"fileName":fileName})
            fileName = '/'+fileName
            file = open(USER_DATA + fileName)
            graf.update({"title":json.load(file)["title"]})
            grafs.append(graf)
    return render_template('home.html', grafs = grafs)

@app.route("/c1", methods=['GET', 'POST'])
def creation_part1():
    form = CreaGraph1()

    if request.method == 'POST' and form.validate_on_submit():
        file = form.data_file.data
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            session['messages'] = [filename, form.graphType.data]
            return redirect('c2')
        flash("File non supportato", "error")

    return render_template("crea_parte1.html", form = form)

@app.route('/c2', methods=["GET", "POST"])
def creation_part2():
    form = CreaGraph2()

    filename = session['messages'][0]
    graphType = session['messages'][1]
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
        asseY2Data = None
        if form.asseY2.data != None:
            asseY2Data = df[form.asseY2.data].to_list()

        data_to_write = {"title": form.title.data,
                        "columns": form.cols.data,
                        "type": [form.graphTypeY1.data, form.graphTypeY2.data],
                        "asseX": form.asseX.data,
                        "asseXData": df[form.asseX.data].to_list(),
                        "asseY1": form.asseY1.data,
                        "asseY1Data": df[form.asseY1.data].to_list(),
                        "asseY2": form.asseY2.data,
                        "asseY2Data": asseY2Data,
                        "secondary": form.secondary.data,
                        "color": [form.colorY1.data, form.colorY1.data]
                        }
                #USER_DATA+"/"+session["username"]+"_"+get_random_string(4)+".json"
        with open(USER_DATA+"/"+get_random_string(4)+".json", "w") as outfile:
            json.dump(data_to_write, outfile)
        delete_file_from_path(UPLOAD_FOLDER +'/'+ filename)
        return redirect("/home")
    form.y2.data = None
    return render_template('crea_parte2.html', form = form, col = colonne)

@app.route('/v/<file>', methods=["GET", "POST"])
def visualizza_grafico(file):

    df = None
    for fileName in os.listdir(USER_DATA):
        if fileName == file:
            fileName = '/'+fileName
            file = open(USER_DATA + fileName)
            jsonData = json.load(file)
            break

    if jsonData["type"] != "Pie":

        if jsonData["asseY2"] == None:
            data = {jsonData["asseX"] : jsonData["asseXData"], jsonData["asseY1"] : jsonData["asseY1Data"]}
            df = pd.DataFrame(data)
            x_data= df[jsonData["asseX"]]
            x_titolo= jsonData["asseX"]
            y_data = [df[jsonData["asseY1"]]]
            y_tipo= [jsonData["type"][0]]
            y_nome= [jsonData["asseY1"]]
            y_titolo= jsonData["asseY1"]
            titolo= jsonData["title"]
            secondary= [False]
            color = jsonData["color"]
        else:
            data = {jsonData["asseX"] : jsonData["asseXData"], jsonData["asseY1"] : jsonData["asseY1Data"], jsonData["asseY2"] : jsonData["asseY2Data"]}
            df = pd.DataFrame(data)
            x_data= df[jsonData["asseX"]]
            x_titolo= jsonData["asseX"]
            y_data = [df[jsonData["asseY1"]], df[jsonData["asseY2"]]]
            y_tipo= [jsonData["type"][0], jsonData["type"][1]]
            y_nome= [jsonData["asseY1"], jsonData["asseY2"]]
            y_titolo= [jsonData["asseY1"], jsonData["asseY2"]]
            titolo= jsonData["title"]
            secondary= [False, jsonData["secondary"]]
            color = jsonData["color"]
        graphJSON = json.dumps(plot_graf_2y(x_data= x_data,
                                    x_titolo= x_titolo,
                                    y_data = y_data,
                                    y_tipo= y_tipo,
                                    y_nome= y_nome,
                                    y_titolo= y_titolo,
                                    titolo= titolo,
                                    secondary= secondary,
                                    color= color),
            cls=plotly.utils.PlotlyJSONEncoder)
        


        
    #DA FARE NON FUNZIONA IL GRAFICO A TORTA NON PROVARE AD UTILIZZARLO
    else:
        graphJSON = json.dumps(plot_pie(df[0],
                                            jsonData["asseX"],
                                            jsonData["asseY1"],
                                            jsonData["title"]),
                                cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('visualizza.html', graphJSON = graphJSON)

@app.route('/d/<file>', methods=["GET", "POST"])
def elimina_grafico(file):

    filePath = USER_DATA+'/'+file
    delete_file_from_path(filePath)
    
    return redirect('/home')


if __name__=='__main__':
   app.run(debug=DEBUG)

# Siamo riusciti ad implementare i grafici, purtroppo quello a torta da ancora problemi, ed a visualizzarli salvando i dati in file json.
# La cosa su cui dobbiamo lavorare è lo stile della pagina web.