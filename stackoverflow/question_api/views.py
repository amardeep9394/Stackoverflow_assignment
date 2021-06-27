from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import GetStackExchange
from .models import Question
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authentication import SessionAuthentication
from rest_framework.throttling import AnonRateThrottle
# Create your views here.
EP = 'https://api.stackexchange.com/2.2/{}'  #endpoint for Stackexchange API
def search_form(request):
	return render(request, 'search.html')
def get_all_questions(request):
	
	#print("here")
	param={
		"page": request.GET["q_page"],
		"order": request.GET['order'],
		"tagged" : request.GET["tagged"],
		"site" : "stackoverflow"
	}
	query = request.build_absolute_uri()
	check_data = Question.objects.filter(query=query)
	print(check_data,"amardeeep")
	if check_data.exists():
		print("yes")

		data_set = check_data.first()
		#print(data_set.query)
		#print(data_set.data['items'])
		authentication_classes=[SessionAuthentication]
		throttle_classes = [AnonRateThrottle]
		stack_data = data_set.data['items']
		print(len(stack_data))
		page = request.GET.get('page', 1)
		paginator = Paginator(stack_data, 10)
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)
		return render(request, 'display.html',{'users':users})
	else:
		response = requests.get(EP.format('questions'), params=param)
		json_response = response.json()
		authentication_classes=[SessionAuthentication]
		throttle_classes = [AnonRateThrottle]
		Question.objects.create(query=query, data = json_response )
		stack_data = json_response['items']
		print(len(stack_data))
		page = request.GET.get('page', 1)
		paginator = Paginator(stack_data, 10)
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)
		return render(request, 'display.html',{'users':users})
		
class Query_ques_View(APIView):

	def get(self,request,*args,**kwargs):
		page = self.request.query_params.get("page")
		query = self.request.query_params.get("query")
		sort = self.request.query_params.get("sort")
		order = self.request.query_params.get("order")
		if(sort=="0"):
			sort="desc"
		if(order=="0"):
			order="activity"
		#ques_qs = Questions.objects.filter(query=query)
		#if ques_qs.exists():
		#	ques_object = ques_qs.first()
		#	serialized_data = QuestionSerializer(ques_object)
		#	data = serialized_data.data['data']
		#	return Response(data,status=status.HTTP_200_OK)
		query_ques_res = GetStackExchange()
		query_ques_res = query_ques_res.search(page,query,order,sort)
		return Response(query_ques_res,status=status.HTTP_200_OK)