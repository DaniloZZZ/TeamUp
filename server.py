from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
        f  =  open("team.json")
        data = f.read()
        f.close()
        return json.loads(data)
app.run()
