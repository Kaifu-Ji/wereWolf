from flask import Flask, request, render_template
import configure
import random
import json

app = Flask(__name__)
app.config.from_object(configure)

character = ['狼人'] * 4 + ['村民'] * 4 + ["猎人"] + ["预言家"] + ["女巫"] + ["白痴神"]
current_round = 0
ready = [True] + [False] * 12
alive = [True] * 13

random.shuffle(character)
character = ['上帝'] + character
print(character)
people_killed = dict()
for index, val in enumerate(character):
    if val == '狼人':
        people_killed[index] = 0

print(people_killed)


@app.route('/')
def index():
    return render_template('index.html', name='A')


@app.route('/character')
def choose_character():
    player_id = int(request.args.get('number'))
    ready[player_id] = True
    return json.dumps({'type': character[player_id], 'number': player_id})


@app.route("/wait-others")
def wait_others():
    global ready
    is_ready = sum(ready) > 3
    if is_ready:
        return json.dumps({'ready': True})
    else:
        noready = []
        for index, val in enumerate(ready):
            if not val:
                noready.append(index)
        return json.dumps({'ready': False, 'noReady': noready})


@app.route('/execute-function')
def execute_function():
    role = ["狼人", "女巫", "预言家", "猎人"]
    people_died = 0;
    global current_round
    play_id = int(request.args.get('number'))
    if current_round == 0:
        if play_id in people_killed:
            killed_id = request.args.get('killed', default=0, type=int)
            people_killed[play_id] = killed_id
            ret = people_killed.copy()
            ret['round'] = 'kill'
            for index in people_killed:
                if people_killed[index] == 0:
                    pass
                else:
                    alive[people_killed[index]] = False
                    current_round = 1
            return json.dumps(ret)
        else:
            return json.dumps({'round': 'kill'})
    if current_round == 1:
        print(role)
        for i in range(13):
            if not alive[i]:
                people_died = i
                break
        ret = {'round': 'heal', 'people_killed': people_died}
        if character[play_id] == '女巫':
            function_use = request.args.get('heal', default=-1, type=int)
            if function_use != -1:
                if function_use > 0:
                    alive[function_use] ^= True
                current_round = 2

        return json.dumps(ret)
    if current_round == 2:
        ret = {'round':'check'}
        if character[play_id] == '预言家':
            function_use = request.args.get('check',default=0,type=int)
            if function_use != 0:
                is_good = character[function_use] != '狼人'
                ret['is_good'] = is_good
                current_round = 3
        return json.dumps(ret)
    if current_round == 3:
        return json.dumps({'round':'elect','alive':alive})


app.run(host='0.0.0.0', port=8888)
