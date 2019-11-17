from wtforms import Form, validators, StringField, SubmitField, IntegerField


class IrisQuizForm(Form):
    qualification = IntegerField('Qualification:', validators=[validators.required(), validators.number_range(0, 10)])
    image_1_response = StringField('RealImageValue:', validators=[validators.required()])
    image_2_response = StringField('SynImageValue:', validators=[validators.required()])
