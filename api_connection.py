#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '9837df6bcc2a435cbcfac3698d24db42'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    # request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    if sys.argv[1]:
        request.query = sys.argv[1]
    else: 
        request.query = "how to save the power"

    response = request.getresponse()

   
    data_string= response.read()
    print (data_string)
    data = json.loads(data_string)
    print (data["result"]["parameters"]["date"])
    print (data["result"])
    print (data["id"])
    id_test=data["id"]
    print (id_test[3:5])
    date_test= str(data["result"]["parameters"]["date"])
    date_string =date_test[3:13]
    print (date_string)

    any_test= str(data["result"]["parameters"]["any"])
    any_string =any_test
    print (any_string)
    

    if sys.argv[1]:
        print sys.argv[1]


    p_comment= "python /Users/wangejay/Github/smartoffice/calendar_manage.py "+ date_string +" "+any_string
    os.system(p_comment)

if __name__ == '__main__':
    main()