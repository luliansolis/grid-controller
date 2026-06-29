import flask
import flask_socketio
import mpld3

app = flask.Flask(__name__, template_folder='/mnt/c/Users/seedd/OneDrive/Desktop/MapController/BaseController', static_folder='/mnt/c/Users/seedd/OneDrive/Desktop/MapController/BaseController', static_url_path='')
socketio = flask_socketio.SocketIO(app)

@app.route('/')
def index():
    return flask.render_template('plot.html')

def update_plot(fig):
    html = mpld3.fig_to_html(fig)
    socketio.emit('update', html)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9090)