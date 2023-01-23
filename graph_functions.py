import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from colour import Color

'''
Esempio di chiamata della funzione:

fig = plot_graf_2y(x_data = df_bomaki_mi.Data, 
                                x_titolo= "Data", 
                                y_data= [df_bomaki_mi.Profitto, df_covid_mi.totale_positivi], 
                                y_tipo= tipo, 
                                y_nome= ["Fatturato","Positivi"],
                                y_titolo= ["Fatturato(€)", "Positivi"], 
                                titolo= "Confronto Fatturato per positivi",
                                secondary= [False, True],
                                color=["#829399","#B1CC74"]
                                )
'''
def plot_graf_2y(x_data: pd.Series, x_titolo: str, y_data: list, y_tipo: list, y_nome: list, y_titolo, titolo: str, secondary: list, color=None, hover_data=None, hover_text=None,):

    """
    Funzione che crea un grafico avente la stessa X e 2 y differenti utilizzando 2 assi y
    -------------------------------------------------------------------------------------
    PARAMETRI
    ---------
    x_data: pd.Series
            pd.Series contenente la colonna del df con i valori utilizzati come asse x
    x_titolo:   str
                String utilizzata come titolo dell'asse X
    y_data: list
            lista contenente pd.Series utilizzate per la creazione del grafico
    y_tipo: list
            lista contenente String utilizzate per identificare la tipologia di ogni grafico
    y_nome: list
            lista di String utilizzate per identificare la traccia e nome utilizzato nella legenda
    y_titolo:   list/str
                String/lista contenente 2 String utilizzate per dare un titolo all'asse/agli assi y
    titolo: str
            String utilizzata come titolo del grafico
    secondary:  list
                lista contenente bool False se la traccia si deve basare all'asse sinistra True se si basa sull'asse destra
    color:  list,string,optional
            lista contenente stringhe di colori per ogni traccia, può essere una stringa se c'è una sola traccia, se non specificato i colori saranno dettati da plotly
    hover_data: list, optional 
                (utilizzati i dati contenuti in y_data) altrimenti Lista contenente Liste contenenti pd.Series utilizzati per la visualizzazione on hover
    hover_text: list,optional 
                (vengono visualizzati i dati di hover_data) altrimenti lista contenente String
                    (es: ["mele: %{customdata[0]}, pere: %{customdata[1]}","banane %{customdata[0]}, arance: %{customdata[1]}"])
    """

    #controllo delle eccezzioni (non tutte)
        #controllo che i valori contengano tutti lo stesso numero di valori e che siano delle liste
    if all(tipo is list for tipo in [type(y_data), type(y_tipo), type(y_nome), type(secondary), (type(color) if color  else list)]):
        if any( lung != len(y_data) for lung in [len(y_tipo), len(y_nome), len(secondary)]):
            raise Exception("y_data, y_nome, secondary - devono avere tutti lo stesso numero di parametri")
    else:
        raise Exception("y_data o gli altri parametri (y_nome, secondary, color) non sono delle liste")

    #controlla hover data per scrivere un hover text rappresentante ogniuno di loro in una riga
    if type(hover_data) is list and not hover_text:
        hover_text=[]
        for j in range(len(hover_data)):
            if type(hover_data[j]) is list:
                hover_text.append("")
                for i in range(len(hover_data[j])):
                    hover_text[j] += ' %{customdata['+str(i)+']} <br>'

    #Inizializza fig - può avere 2 assi y
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    #Crea un grafico per ogni Serie data
    for i in range(len(y_data)):

        #Tipo di grafico
        y_tipo_grafico = getattr(go, y_tipo[i])

        #Crea la traccia
        fig.add_trace( y_tipo_grafico
                        (  x=x_data, y=y_data[i], name=y_nome[i], 
                            customdata=np.stack((hover_data[i] if hover_data else y_data[i]), axis=-1), 
                            hovertemplate= hover_text[i] if hover_data else '%{customdata}', marker={"color": (color[i] if color else None)}
                        ), 
                        secondary_y=secondary[i]
                    )

    #Assegna il titolo all'asse y - se sono due il primo elemento sarà il titolo dell'asse sinistra e il secondo quello dell'asse destra
    if type(y_titolo) is list:
        fig.update_yaxes(title_text= y_titolo[0], secondary_y=False)
        fig.update_yaxes(title_text= y_titolo[1], secondary_y=True)
    else:
        fig.update_yaxes(title_text= y_titolo, secondary_y=False)
    
    #Assegna il titolo all'asse x
    fig.update_xaxes(title_text= x_titolo)

    #Assegna il titolo del grafico e modifica la modalita hover
    fig.update_layout(
        title_text=titolo,
        hovermode="x unified"
    )

    return fig


def plot_pie(labels: list, values: list, title: str, hole = None, opacity = None, color = None, hoverinfo = None, textinfo = None):

    """
    Funzione che crea un grafico a torta
    -------------------------------------------------------------------------------------
    PARAMETRI
    ---------
    labels: list
            List contenente i nomi della legenda del grafico
    values: list
            List contenente i valori numerici su cui il grafico si baserà
    titolo: str
            String utilizzata come titolo del grafico
    hole:  numeric, optional
            Valore da 0 a 1 per creare il grafico a ciambella
    opacity: numeric, optional
            Valore da 0 a 1 per creare il grafico con colori più o meno accesi
    color:  string, optional
            stringa contenente un colore a scelta che poi sarà utilizzato per creare una scala del colore inserito
    hover_info: string, optional 
                stringa per scegliere che informazioni mostrare quando il cursore passa sopra ad una fetta del grafico 
    textinfo: string, optional 
                stringa per scegliere che informazioni mostrare all'interno della fetta del grafico
    """

    if any(lung != len(values) for lung in [len(labels)]):
        raise Exception("values, labels - devono avere tutti lo stesso numero di parametri")

    if hole is not None and (type(hole) != int and type(hole) != float):
        raise Exception("hole deve essere un valore numerico")
    
    if hole is not None and (hole<0 or hole>1):
        raise Exception("hole deve essere compreso tra 0 e 1")

    if opacity is not None and (type(opacity) != int and type(opacity) != float):
        raise Exception("opacity deve essere un valore numerico")

    if opacity is not None and (opacity<0 or opacity>1):
        raise Exception("opacity deve essere compreso tra 0 e 1")

    if color is not None and type(color) != str:
        raise Exception("color deve essere una stringa")
    starting_color = Color(color, luminance = 0.95)
    colors = list(starting_color.range_to(Color(color), len(values)))
    colors = list(map(str, colors))
    fake = ["a"] * len(values)

    if hoverinfo is not None and type(hoverinfo) != str:
        raise Exception("hoverinfo, se non è None, deve essere una stringa")

    if textinfo is not None and type(textinfo) != str:
        raise Exception("textinfo, se non è None, deve essere una stringa")

    if type(title) != str:
        raise Exception("title deve essere una stringa")
    
    fig = go.Figure()
    if color is not None:
        fig.add_trace(go.Pie(labels=labels, values=values, opacity=opacity, marker={"colors": fake}, hole = hole, hoverinfo=hoverinfo, textinfo=textinfo))
        fig.update_layout(title=title)
        fig.data[0].values = sorted(fig.data[0].values)
        fig.data[0].marker.colors = colors
    else:
        fig.add_trace(go.Pie(labels=labels, values=values, opacity=opacity, hole = hole, hoverinfo=hoverinfo, textinfo=textinfo))
        fig.update_layout(title=title)
    return fig