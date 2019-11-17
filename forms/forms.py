from wtforms import Form, validators, StringField, SubmitField, IntegerField


class IrisQuizForm(Form):
    qualification = IntegerField('Qualification:', validators=[validators.required(), validators.number_range(0, 10)])
    img_1_response = StringField('RealImageValue:', validators=[validators.required()])
    img_2_response = StringField('SynImageValue:', validators=[validators.required()])
