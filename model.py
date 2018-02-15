# -*- coding: utf-8 -*-
import traceback
import settings
import pandas as pd
import numpy as np
import json,random,gensim
import requests
from operator import itemgetter
from gensim.models import KeyedVectors
from scipy.spatial.distance import cosine


def mapping(df):
    d = df['experience_month_total']/df['age']
    try:
        d+=df['work_history'].apply(lambda x: len((x)))
        return d
    except Exception as e:
        print e
        traceback.format_exc()
        return 0

class Model:
    def __init__(self):
        print "Model: reading data"
        self.data = pd.read_json('res.json')
        self.answ = pd.read_csv('Answers-Data.csv',sep=';')
        self.ocean= pd.read_csv('ocean.csv',index_col='idx')
        self.w2v= pd.read_csv('w2v.csv')
        self.sauce_id = 3614
        self.sauce_key = 'som2es26nn1ieugrdjlnfnv9vn'
        print "Model: done reading data"

    def filter(self,names):
        res = {}
        for n in names:
            _n  = n.replace(' ','').title()
            print _n
            vals = self.data.loc[self.data['profession_tree_name'] == _n][:35]
            print "Hard filter: %i results"%len(vals)
            if len(vals)>0:
                print self.sort(vals)[:5]
                res[n] = self.sort(vals)[:7].to_dict(orient='records')
            else:
                res[n] = vals.to_dict(orient='records')
        return res

    def sort(self,df):
        new = df.assign(f = mapping(df))
        f = np.array(new['f'])
        f/=max(f)
        oc = self.ocean[:len(f)]
        l = len(f)
        n = random.randint(0,l)
        print n
        mat = self.ocean.as_matrix()
        oced = []
        for i in range(l):
            dic = np.sum((mat[n]-mat[i])**2)
            oced.append(dic)
        oced =np.array(oced)
        mat = self.w2v.as_matrix()
        v= []
        for i in range(l):
            dic =cosine(mat[n],mat[i])
            v.append(1./(0.5+dic))
        v = np.array(v)
        v/=max(v)
        print mat.shape
        print oced,v
        k = 1./3.
        f= k*f + k*oced + k*v
        new['f'] = f
        res= new.sort_values('f',ascending=False)
        return res.reset_index(drop=True)


    def find(self,team):
        members = self.filter(team['people'])
        #save candidates to file
        f = open(settings.TEAMS_DIR+team['name']+'.json','w+')
        f.write(json.dumps(members))
        f.close()

    def auth(self):
        try:
            credentials = {
                'customer_id': self.sauce_id,
                'api_key': self.sauce_key
            }
            response = requests.post('https://api.applymagicsauce.com/auth', json=credentials)
            response.raise_for_status()
            self.sauce_token = response.json()['token']
            return response.json()['token']
        except requests.exceptions.HTTPError as e:
            print e.response.json()

    def predict_from_text(self, text):
        try:
            response = requests.post(url='https://api.applymagicsauce.com/text',
                                     params={
                                         'source': 'OTHER'
                                     },
                                     data=text,
                                     headers={'X-Auth-Token':self.sauce_token})
            response.raise_for_status()
            dic =sorted(response.json()['predictions'],key=itemgetter('trait'))
            vec = [a['value'] for a in dic]
            # return everything except age
            return response.json(),vec[1:]
        except requests.exceptions.HTTPError as e:
            print e.response.json()

if __name__=='__main__':
    model = Model()
    '''
    model.auth()
    print "fetch OCEAN types for every record in Answers.csv"
    for i in range(50):
        text = model.answ.iloc[i]['QN1-about']
        text += model.answ.iloc[i]['QN2-passion']
        dic,vec= model.predict_from_text(text)
        res.append(vec)
        print i,vec
    df = pd.DataFrame(res)
    df.to_csv('ocean.csv')
    goog = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz',
                                      binary=True, limit=1500000)

    res = []
    for i in range(50):
        text = model.answ.iloc[i]['QN1-about']
        text += model.answ.iloc[i]['QN2-passion']
        vec = np.zeros(300)
        print i
        ws = text.split()
        j=0
        sk = []
        for w in ws:
            if len(w)>2:
                try:
                    vec+=goog[w]
                except:
                    sk.append(w)
                    j+=1
        print "words total:%i skipped: %i"%(len(ws),j)
        print sk
        res.append(vec)
        print i
    df = pd.DataFrame(res)
    df.to_csv('v2w.csv')
    '''
    model.filter([u' менеджер',u'юрист'])

