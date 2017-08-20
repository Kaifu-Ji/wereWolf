from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'windroc-nwpc-project'

socketio = SocketIO(app)


@app.route('/data',methods=['GET','POST'])
def data():
    if request.method == 'GET':
        return "This is a response for" + request.args.get('id')
    else:
        return "This is a response to post request" + request.args.get('id')


@app.route('/')
def get_index_page():
    return '''
        <body>
            <button onclick="
            var xhr = new XMLHttpRequest();
        setInterval(function(){
        xhr.open('get','/data?id=3',true);
        xhr.onreadystatechange = function(){
            document.getElementById('A2').innerHTML = xhr.responseText;
        };
        xhr.send();
    },5000);
            ">click me</button>
            <p><b>Status text:</b>
            <span id="A2"></span>
            </p>
        </body>
    '''


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5101)
