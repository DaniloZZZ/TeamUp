import pandas as pd
import json
from flask import Flask

class Model:
    def __init__(self):
        print "reading data"
        self.data = pd.read_json('resumes_edited.json')
        print "done"
        app.run()

    def filter(names):
        res = []
        for n in names:
            vals = self.data.loc[self.data['profession_tree_name'] == n]
            print vals
            res.append(vals[:5])
        f = open('team.json','w+')
        f.write(json.dumps(res))
        f.close()
        return res
    def find(team):
        return self.filter(team['people'])




