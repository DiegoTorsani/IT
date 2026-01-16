from flask import Flask, render_template, request, redirect, url_for, g
import db

app = Flask(__name__)
app.config['DATABASE'] = 'youtube_like.db'

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/channels')
def channel_list():
    channels = db.get_db().execute('SELECT * FROM canali').fetchall()
    return render_template('channel_list.html', channels=channels)

@app.route('/channels/<int:channel_id>')
def channel_detail(channel_id):
    channel = db.get_db().execute('SELECT * FROM canali WHERE id = ?', (channel_id,)).fetchone()
    videos = db.get_db().execute('SELECT * FROM video WHERE canale_id = ?', (channel_id,)).fetchall()
    return render_template('channel_detail.html', channel=channel, videos=videos)

@app.route('/add_channel', methods=['GET', 'POST'])
def add_channel():
    if request.method == 'POST':
        nome = request.form['nome']
        numero_iscritti = request.form.get('numero_iscritti', 0)
        categoria = request.form['categoria']
        db.get_db().execute('INSERT INTO canali (nome, numero_iscritti, categoria) VALUES (?, ?, ?)', (nome, numero_iscritti, categoria))
        db.get_db().commit()
        return redirect(url_for('channel_list'))
    return render_template('add_channel.html')

@app.route('/add_video/<int:channel_id>', methods=['GET', 'POST'])
def add_video(channel_id):
    if request.method == 'POST':
        titolo = request.form['titolo']
        durata = request.form['durata']
        immagine = request.form.get('immagine', '')
        db.get_db().execute('INSERT INTO video (canale_id, titolo, durata, immagine) VALUES (?, ?, ?, ?)', (channel_id, titolo, durata, immagine))
        db.get_db().commit()
        return redirect(url_for('channel_detail', channel_id=channel_id))
    return render_template('add_video.html', channel_id=channel_id)

if __name__ == '__main__':
    app.run(debug=True)