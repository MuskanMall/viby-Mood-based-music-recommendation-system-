from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import ValidationError

class CaptureForm(FlaskForm):
    picture = FileField('Capture', validators = [FileAllowed(['jpg'])])
    capture = SubmitField('Capture')


class MoodForm(FlaskForm):
    mood = StringField('Mood')
    submit = SubmitField('Submit')
    user_consent = RadioField('User_consent', choices=[('Yes','Yes'),('No','No')])

    def validate_mood(self, mood):
        moods = ['angry', 'happy', 'sad', 'surprise', 'neutral']
        if mood.data.lower() not in moods:
            raise ValidationError('Please enter a valid mood.')

def get_artist_choices(file_path):
    try:
        with open(file_path, 'r') as file:
            artists = file.readlines()
        choices = [('', '')]  # Blank option
        choices += [(artist.strip(), artist.strip()) for artist in artists if artist.strip()]
        return choices
    except IOError:
        # Handle the error if the file doesn't exist or can't be read
        raise Exception("Error reading artists file")
        return []


class ArtistForm(FlaskForm):
    artist_choices = get_artist_choices('/Users/muskanmall/Desktop/capstone_website/cs_web/static/artists.txt')
    # Dropdown fields for artists
    artist1 = SelectField('Artist 1', choices=artist_choices)
    artist2 = SelectField('Artist 2', choices=artist_choices)
    artist3 = SelectField('Artist 3', choices=artist_choices)
    artist4 = SelectField('Artist 4', choices=artist_choices)
    artist5 = SelectField('Artist 5', choices=artist_choices)

    submit = SubmitField('Submit')

    def validate_artist1(self, artist1):
        if artist1.data == '':
            raise ValidationError('Please select an artist.')
        
    def validate_artist2(self, artist2):
        if artist2.data == '':
            raise ValidationError('Please select an artist.')
        
    def validate_artist3(self, artist3):
        if artist3.data == '':
            raise ValidationError('Please select an artist.')
        
    def validate_artist4(self, artist4):
        if artist4.data == '':
            raise ValidationError('Please select an artist.')
        
    def validate_artist5(self, artist5):
        if artist5.data == '':
            raise ValidationError('Please select an artist.')
