import pandas as pd
import json

class Model:
    def __init__(self):
        print "reading data"
        self.data = pd.read_json('res.json')
        print "done"

    def filter(self,names):
        res = {}
        for n in names:
            _n  = n.title().replace(' ','')
            print _n
            vals = self.data.loc[self.data['profession_tree_name'] == _n]
            print vals[:5]
            res[n] = vals[:5].to_dict(orient='records')
        f = open('team.json','w+')
        f.write(json.dumps(res))
        f.close()
        return res
    def find(self,team):
        return self.filter(team['people'])




