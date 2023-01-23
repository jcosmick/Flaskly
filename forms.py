from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length, InputRequired, Regexp, Optional
from wtforms.widgets.html5 import ColorInput
from wtforms.widgets import CheckboxInput, ListWidget

class CreaGraph1(FlaskForm):
    graphType = SelectField('Tipo grafico', 
                            coerce=str, 
                            choices=[("Pie","Pie"),("Cartesian","Cartesian")],
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

    y2 = SelectMultipleField(
        'Doppio asse Y',
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=True),
        coerce=int,
        choices=[(1, "Doppio asse Y")])
    
    asseX = RadioField('Asse X',
                        validators=[InputRequired(), DataRequired()])
    asseY1 = RadioField('Asse Y',
                        validators=[InputRequired(), DataRequired()])
    asseY2 = RadioField('Asse Y2',validators=[Optional()])
    color = StringField(widget=ColorInput())
    submit = SubmitField("Salva")

    def y2_checked_not_null(self):
        #Se è stata aggiunta una seconda asse y viene eseguito il controllo:
        #   La selezione della colonna per la seconda Y non deve essere nulla
        if bool(self.y2.data):
            if self.asseY2.data == "None":
                return False

    def max_cols_selected(self):
        #Se il numero di scelte è maggiore a tre ritorno False (la validazion non è andata a buon fine)
        if len(self.cols.data) > 3:
            self.cols.errors.append("Non puoi selezionare più di 3 colonne")
            return False

    def validate_on_submit(self):
        #Eseguo il normale controllo
        rv = super().validate_on_submit()

        #Eseguo i controlli custom
        rv = self.y2_checked_not_null()
        rv = self.max_cols_selected()

        #Se la validazione non va a buon fine ritorno False
        if not rv:
            return False

        return True




