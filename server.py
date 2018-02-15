from flask import Flask,jsonify,request,abort
import settings
import json
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def hello_world():
    team_name = request.args.get('team')
    print team_name
    try:
        #f  =  open("team_"+team_name+".json")
        f  =  open(settings.TEAMS_DIR+team_name+".json")
        data = f.read()
        f.close()
        return jsonify(json.loads(data))
    except:
        print failed
        abrort(404)
    #return str(cwjson.loads(data))

app.run(host='0.0.0.0',threaded=True,debug=True)
