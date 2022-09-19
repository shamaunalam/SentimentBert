from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.conf import settings
import pandas as pd
import os
import firebase_admin
from firebase_admin import credentials,firestore

cd = credentials.Certificate(os.path.join(settings.BASE_DIR,"mood-lists-c75ee-firebase-adminsdk-zztep-bcbc10e4c2.json"))
firebase_admin.initialize_app(cd)

# Create your views here.
@api_view(['GET'])
def index(request):
    sentiment_analysis = settings.SENTIMENT_ANALYSIS
    datab = firestore.client()
    usersref = datab.collection(u'Users')
    docs = usersref.stream()
    
    fname=[]
    msg = []

    for doc in docs:
        d = doc.to_dict()
        fname.append(d['firstname'])
        msg.append(d['msg'])

    _dict_ = {'firstname':fname,'msg':msg}
    dict_ = dict()
    for i,sent in enumerate(_dict_['msg']):
        sentiment = sentiment_analysis(sent,truncation=True)
        dict_.update({i:{'comment':sent,'sentiment':sentiment[0]['label']}})
        #print(dict_)
    return Response(dict_)