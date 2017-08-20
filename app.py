from flask import Flask, request, render_template
import configure
import random
import json

app = Flask(__name__)
app.config.from_object(configure)

character = ['狼人'] * 4 + ['村民'] * 4 + ["猎人"] + ["预言家"] + ["女巫"] + ["白痴神"]
ready = [True] + [False] * 12

random.shuffle(character)
character = ['上帝'] + character
print(character)


@app.route('/')
def index():
    return render_template('index.html', name='A')


@app.route('/character')
def choose_character():
    player_id = int(request.args.get('number'))
    ready[player_id] = True
    return json.dumps({'type':character[player_id],'number':player_id})


@app.route("/wait-others")
def wait_others():
    global ready
    is_ready = sum(ready) > 2
    if is_ready:
        return json.dumps({'ready':True})
    else:
        noready = []
        for index,val in enumerate(ready):
            if not val:
                noready.append(index)
        return json.dumps({'ready':False,'noReady':noready})
app.run(host='0.0.0.0', port=8888)
