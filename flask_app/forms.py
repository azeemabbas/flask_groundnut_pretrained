from flask_wtf import FlaskForm
from wtforms import SubmitField, MultipleFileField


class UploadForm(FlaskForm):
    image        = MultipleFileField('Choose an Image File and Press Upload Button')#, validators=[Regexp('^[^/\\]\.jpg$')])
    submit = SubmitField("Upload Images")

    def validate_image(self, image):
        if image.data:
            image.data = re.sub(r'[^a-z0-9_.-]', '_', image.data)