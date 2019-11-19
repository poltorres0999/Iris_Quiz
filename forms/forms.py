from wtforms import Form, validators, StringField, SubmitField, IntegerField


class IrisQuizForm(Form):
    qualification = IntegerField('Qualification:', validators=[validators.required(), validators.number_range(0, 10)])
    img_1_response = StringField('RealImageValue:', validators=[validators.required()])
    img_2_response = StringField('SynImageValue:', validators=[validators.required()])


class UploadIrisImageForm(Form):
    img_width = StringField('ImgWidth:', validators=[validators.required()])
    img_height = StringField('ImgHeight:', validators=[validators.required()])
    img_type = StringField('ImgType:', validators=[validators.required()])
