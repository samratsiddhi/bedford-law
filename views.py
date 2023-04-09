from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from benfordslaw import benfordslaw
import pandas as pd 
import numpy as np
import json

globalmessage = "message"

@view_config(route_name='index', renderer='template/selectcsv.html')
def index(request):
   message = globals()['globalmessage']
   globals()['globalmessage'] = 'message'
   return {'message':message}

@view_config(route_name='output', renderer='template/output.html')
def output(request):
   message = globals()['globalmessage']
   globals()['globalmessage'] = 'message'
   return {'message':message}


@view_config(route_name='verify')
def add(request):
    location = request.params['location']
   
    if location.endswith('.csv') == False:
        globals()['globalmessage'] = "The dataset has to be a csv file "
        return HTTPFound(location='/output')
    
    try:
        df = pd.read_csv(location)
        read = 0
    except:
        read = 1
    if read == 1:
        globals()['globalmessage'] = "Unable read file, please check the path"
        return HTTPFound(location='/output')
    columns = df.shape[1]

    if columns == 1:
        bl = benfordslaw(alpha=0.05)
        X = df.values
        results = bl.fit(X)
        if results['P_significant'] == False:
            # new_res = results['percentage_emp'].tolist()
            # res = json.dumps(new_res)
            dictionary = {'status':'true', 'message':'"The dataset does not conform to the Bedfords Law on first digits"'}
            jsonString = json.dumps(dictionary, indent=4)

            globals()['globalmessage'] = jsonString
            return HTTPFound(location='/output')
 
        else:
            globals()['globalmessage'] = "The dataset does not conform to the Bedfords Law on first digits"
            return HTTPFound(location='/output')
    else:
        globals()['globalmessage'] = "File has more than 1 column. Please select another file "
        return HTTPFound(location='/output')
