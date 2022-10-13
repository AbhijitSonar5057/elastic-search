from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import requests
import json
from home.models import *
from elasticsearch_dsl import Q
from .documents import *
from .serializers import *
from rest_framework.response import Response
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)

def generate_random_data():
    url = 'https://newsapi.org/v2/everything?q=Apple&from=2022-10-11&to=2022-10-23&sortBy=popularity&apiKey=81167d8c84fe4110bada2bc8fc5280a3'
    r = requests.get(url)
    payload = json.loads(r.text)
    count = 1
    for data in payload.get('articles'):
        print(count)
        ElasticDemo.objects.create(
            title = data.get('title'),
            content = data.get('description')
        )

def index(request):
    generate_random_data()
    return JsonResponse({'status' : 200})




class PublisherDocumentView(DocumentViewSet):
    document = NewsDocument
    serializer_class = NewsDocumentSerializer
    # lookup_field = 'first_name'
    fielddata=True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
   
    search_fields = (
        'title',
        'content',
    )
    multi_match_search_fields = (
       'title',
        'content',
    )
    filter_fields = {
       'title' : 'title',
        'content' : 'content',
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id'  ,)
        
  

class TestQuery(DocumentViewSet):
    document = NewsDocument
    serializer_class = NewsDocumentSerializer

    def list(self, request):
        li=[]

        #multimatch
        # query = 'Airpods'
        # q = Q(
        #     'multi_match',
        #     query=query,
        #     fields=[
        #         'title'
        #     ])
        # search = NewsDocument.search().query(q)
        # response = search.execute()
        # # print all the hits
        # for hit in search:
        #     print("========>>>>>>>>",hit.title)
        #     Documents = { "title" :hit.title }          
        #     li.append(Documents)

        #bool
        query = 'Apple'
        q = Q(
            'bool',
        must=[
            Q('match', title='tesla'),
        ],
        must_not=[
            Q('match', title='ruby'),
            Q('match', content='javascript'),
        ],
        should=[
            Q('match', title=query),
            Q('match', content=query),
        ],
        minimum_should_match=1)
        search = NewsDocument.search().query(q)
        response = search.execute()
        # print all the hits
        for hit in search:
            Documents = { "title" :hit.title }          
            li.append(Documents)

        return Response(li)
    

class SearchCategories(DocumentViewSet):
    serializer_class = NewsDocumentSerializer
    document_class = NewsDocument
    try:
        def list(self, query):
            # q = Q(
            # 'multi_match', query=query,
            # fields=[
            #     'name',
            #     'description',
            # ], fuzziness='auto')


        # query = 'Apple'
        # q = Q(
        #     'bool',
        # must=[
        #     Q('match', title='tesla'),
        # ],
        # must_not=[
        #     Q('match', title='ruby'),
        #     Q('match', content='javascript'),
        # ],
        # should=[
        #     Q('match', title=query),
        #     Q('match', content=query),
        # ],
        # minimum_should_match=1)
        # search = NewsDocument.search().query(q)
        # response = search.execute()
        # # print all the hits
        # for hit in search:
        #     Documents = { "title" :hit.title }          
        #     li.append(Documents)


                
            search = NewsDocument.search().query(q)
            response = search.execute()
            li=[]
            # print all the hits
            for hit in response:
                Documents = { "title" :hit.title }          
                li.append(Documents)
            return Response(li)

    except Exception as e:
        print(e)