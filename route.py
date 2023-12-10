from flask import Flask, render_template, flash, redirect, url_for, request
from forms import CaptureForm, MoodForm, ArtistForm
import os
import RealTimeEMotionDetection 
from spotify import get_playlist_url
app =Flask(__name__)
app.config['SECRET_KEY'] = '6b02adc4284f85698f6f61abe5fca402'

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Home')


@app.route('/capture', methods=['GET','POST'])
def capture():
    form = CaptureForm()

    if form.validate_on_submit():
        picture_file = form.picture.data
        picture_file.save(os.path.join(app.root_path, 'static/user_image/user.jpg'))
        flash('Image Captured')
        Detected_emotion = RealTimeEMotionDetection.emotion_detection('/Users/muskanmall/Desktop/capstone_website/cs_web/static/user_image/user.jpg')
        try:
            with open('static/mood_value.txt', 'w') as f:
                f.write(Detected_emotion)
        except IOError:
            flash('Error saving mood value. Please try again.', 'error')

        return redirect(url_for('mood'))
    
    return render_template('capture.html', title='Capture', form=form )

@app.route('/mood', methods=['GET', 'POST'])
def mood():
    form = MoodForm()
    try:
        with open('static/mood_value.txt', 'r') as f:
            mood_detected = f.read().strip()
    except IOError:
        mood_detected = None
        flash('Error reading mood value. Please try again.', 'error')

    if form.validate_on_submit():
        if form.user_consent.data == 'yes':
            flash('Great! You are happy with the mood: ' + mood_detected, 'success')
        else:
            new_mood = form.mood.data.lower()
            if new_mood:
                mood_detected = new_mood  
                try:
                    with open('static/mood_value.txt', 'w') as f:
                        f.write(new_mood)
                    flash('New mood set to: ' + new_mood, 'info')
                except IOError:
                    flash('Error saving new mood. Please try again.', 'error')
            else:
                flash('Please enter a new mood.', 'warning')

        # Redirect happens here, after handling both 'yes' and 'no' cases
        return redirect(url_for('artist'))
    elif request.method == 'GET':
        form.mood.data = mood_detected
    return render_template('mood.html', title='Mood', form=form, mood_detected=mood_detected)




@app.route('/artist', methods=['GET','POST'])
def artist():
    form = ArtistForm()
    if form.validate_on_submit():
        selected_artists = [
            form.artist1.data,
            form.artist2.data,
            form.artist3.data,
            form.artist4.data,
            form.artist5.data
        ]
        try:
            with open('static/mood_value.txt', 'r') as f:
                mood_detected = f.read().strip()
        except IOError:
            mood_detected = None
            flash('Error reading mood value. Please try again.', 'error')
        selected_artists = set(selected_artists)
        playlist_url = get_playlist_url(selected_artists, mood_detected)
        return redirect(playlist_url)
    return render_template('artist.html', title='Artist', form=form)

# @app.route('/playlist/<path:url>')
# def playlist(url):
#     # will display the playlist, if we cant redirect to spotify page
#     # try to display the playlist on the page
#     return render_template('playlist.html', title='Playlist', url=url)


if __name__ == '__main__':
    app.run(debug=True)
