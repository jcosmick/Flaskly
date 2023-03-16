from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField, RadioField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired, Regexp, Optional
from wtforms.widgets import  CheckboxInput, ListWidget
from wtforms.widgets import ColorInput

class CreaGraph1(FlaskForm):
    graphType = SelectField('Tipo grafico', 
                            coerce=str, 
                            choices=[("Cartesian","Cartesian"),
                                     ("Pie","Pie")
                                    ],
                            validators= [InputRequired()])
    data_file = FileField('Csv file', validators= [DataRequired()])
    submit = SubmitField("Crea")

class CreaGraph2(FlaskForm):
    title = StringField('Titolo',
                    validators=[InputRequired(),
                                Length(1,20), 
                                DataRequired(),
                                Regexp(r'^[\w.@+-]+$')],
                                render_kw={"placeholder": "Titolo"})
    cols = SelectMultipleField(
        'Colonne',
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=True))

    y2 = BooleanField(
        'Doppio asse Y'
        )
    
    asseX = RadioField('Asse X',
                        validators=[InputRequired(), DataRequired()])
    graphTypeY1 = SelectField('Tipo grafico', 
                        coerce=str, 
                        choices=[("Scatter","Scatter"),
                                    ("Bar","Bar")],
                        validators= [InputRequired()])
    asseY1 = RadioField('Asse Y',
                        validators=[InputRequired(), DataRequired()])
    graphTypeY2 = SelectField('Tipo grafico', 
                    coerce=str, 
                    choices=[("Scatter","Scatter"),
                                ("Bar","Bar")],
                    validators= [InputRequired()])
    asseY2 = RadioField('Asse Y2',validators=[Optional()])

    secondary = BooleanField(
        'Asse y secondaria'
        )

    colorY1 = StringField("Colore: ",widget=ColorInput())
    colorY2 = StringField("Colore: ",widget=ColorInput())
    submit = SubmitField("Salva")

    def y2_checked_not_null(self):
        """Se è stata aggiunta una seconda asse y viene eseguito il controllo:
           La selezione della colonna per la seconda Y non deve essere nulla"""
        if self.y2.data:
            if self.asseY2.data == None:
                self.asseY2.errors.append("Seleziona una colonna per il secondo asse Y")
                return False
            else:
                return True
        else:
            self.asseY2.data = None
            return True

    def max_cols_selected(self):
        #Se il numero di scelte è maggiore a tre ritorno False (la validazion non è andata a buon fine)
        if len(self.cols.data) > 3:
            self.cols.errors.append("Non puoi selezionare più di 3 colonne")
            return False
        else:
            return True

    def validate_on_submit(self):
        #Eseguo il normale controllo
        return super().validate_on_submit() and self.y2_checked_not_null() and self.max_cols_selected()
