from flask import Flask,jsonify,request,abort
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    team_name = request.args.get('team')
    print team_name
    try:
        #f  =  open("team_"+team_name+".json")
        f  =  open("team.json")
        data = f.read()
        f.close()
        return jsonify(json.loads(data))
    except:
        print failed
        abrort(404)
    #return str(cwjson.loads(data))

app.run()
