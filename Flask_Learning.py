from flask import Flask
import configure

app = Flask(__name__)
app.config.from_object(configure)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/article/<article_id>')
def article(article_id):
    return "The article you want to read has id %s" % (article_id)


if __name__ == '__main__':
    app.run(port=3000,host='192.168.0.11')
