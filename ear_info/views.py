from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render,HttpResponse
from django.template.loader import get_template
from datetime import datetime
from ear_info.models import Earthquake
from ear_info.serializers import EarthquakeSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
import json

def EarthquakeList(request):
	template = get_template('earthquake_list_page.html')
	now = datetime.now
	html = template.render(locals())
	return HttpResponse(html)

def WidgeList(request):
	template = get_template('widget_page.html')
	now = datetime.now
	html = template.render(locals())
	return HttpResponse(html)

def ShowMap(request):
	template = get_template('test.html')
	html = template.render(locals())
	return HttpResponse(html)

# Create your views here.
class EarthquakeViewSet(viewsets.ModelViewSet):
	queryset = Earthquake.objects.all()
	serializer_class = EarthquakeSerializer
	

def get_earthquake_data(request):
	'''
	专门处理在服务器资产列表里面的表格信息的方法
	:param request: 
	:return: 
	'''
	if request.method == "GET":
		print(request.GET)
		limit = request.GET.get('limit')   # how many items per page
		offset = request.GET.get('offset')  # how many items in total in the DB
		search = request.GET.get('search')
		sort_column = request.GET.get('sort')   # which column need to sort
		order = request.GET.get('order')	  # ascending or descending
		if search:	#	判断是否有搜索字 id=search,ear_id=search,s_year=search,ear_time=search,ear_longitude=search,ear_latitude=search,ear_scale=search,ear_deep=search,ear_epicenter_pos=search
			if '=' in search:
				if '編號=' in search or 'id=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(id__contains=search1))
				elif '地震編號=' in search or 'ear_id=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(ear_id__contains=search1))
				elif '年份=' in search or 's_year=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(s_year__contains=search1))
				elif '台灣時間=' in search or 'ear_time=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(ear_time__contains=search1))
				elif '經度=' in search or 'ear_lg=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(ear_longitude__contains=search1))
				elif '緯度=' in search or 'ear_lt=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(ear_latitude__contains=search1))
				elif '規模=' in search or 'ear_scale=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(ear_scale__contains=search1))
				elif '深度=' in search or 'ear_deep=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(ear_deep__contains=search1))
				elif '震央位置=' in search or 'ear_pos=' in search:
					search1=search.split('=')[1]
					all_records = Earthquake.objects.filter(Q(ear_epicenter_pos__contains=search1))
				else:
					all_records = Earthquake.objects.filter(Q(id__contains=search) | 
														Q(ear_id__contains=search) | 
														Q(s_year__contains=search) |
														Q(ear_time__contains=search) |
														Q(ear_longitude__contains=search) |
														Q(ear_latitude__contains=search) |
														Q(ear_scale__contains=search) |
														Q(ear_deep__contains=search) |
														Q(ear_epicenter_pos__contains=search))
			else:
				print('= not it')
				all_records = Earthquake.objects.filter(Q(id__contains=search) | 
														Q(ear_id__contains=search) | 
														Q(s_year__contains=search) |
														Q(ear_time__contains=search) |
														Q(ear_longitude__contains=search) |
														Q(ear_latitude__contains=search) |
														Q(ear_scale__contains=search) |
														Q(ear_deep__contains=search) |
														Q(ear_epicenter_pos__contains=search))
		else:
			all_records = Earthquake.objects.all()   # must be wirte the line code here
		
		if sort_column:   # 判断是否有排序需求
			sort_column = sort_column.replace('earthquake_', '')	
			if sort_column in ['id','ear_id','s_year','ear_time','ear_longitude','ear_latitude','ear_scale','ear_deep','ear_epicenter_pos']:   # 如果排序的列表在这些内容里面
				if order == 'desc':   # 如果排序是反向
					sort_column = '-%s' % (sort_column)
				all_records = all_records.order_by(sort_column)

		all_records_count=all_records.count()

		if not offset:
			offset = 0

		if limit == "-1":
			response_data = {'total':all_records_count,'rows':[]}
			for earthquake in all_records:
				response_data['rows'].append({
					"earthquake_id": int(earthquake.id) if int(earthquake.id) else "",
					"earthquake_ear_id" : earthquake.ear_id if earthquake.ear_id else "",
					"earthquake_s_year": int(earthquake.s_year) if int(earthquake.s_year) else "",
					"earthquake_ear_time": earthquake.ear_time if earthquake.ear_time else "",
					"earthquake_ear_longitude": float(earthquake.ear_longitude) if float(earthquake.ear_longitude) else "",
					"earthquake_ear_latitude": float(earthquake.ear_latitude) if float(earthquake.ear_latitude) else "",
					"earthquake_ear_scale": float(earthquake.ear_scale) if float(earthquake.ear_scale) else "",
					"earthquake_ear_deep": float(earthquake.ear_deep) if float(earthquake.ear_deep) else "",
					"earthquake_ear_epicenter_pos":earthquake.ear_epicenter_pos if earthquake.ear_epicenter_pos else "",
				})
			return  HttpResponse(json.dumps(response_data), content_type="application/json")

		if not limit:
			limit = 10	# 默认是每页20行的内容，与前端默认行数一致

		pageinator = Paginator(all_records, limit)   # 开始做分页

		page = int(int(offset) / int(limit) + 1)	
		response_data = {'total':all_records_count,'rows':[]}   # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容

		for earthquake in pageinator.page(page):
			# 下面这些earthquake_开头的key，都是我们在前端定义好了的，前后端必须一致，前端才能接受到数据并且请求.
			response_data['rows'].append({
				"earthquake_id": earthquake.id if earthquake.id else "",
				"earthquake_ear_id" : earthquake.ear_id if earthquake.ear_id else "",
				"earthquake_s_year": earthquake.s_year if earthquake.s_year else "",
				"earthquake_ear_time": earthquake.ear_time if earthquake.ear_time else "",
				"earthquake_ear_longitude": earthquake.ear_longitude if earthquake.ear_longitude else "",
				"earthquake_ear_latitude": earthquake.ear_latitude if earthquake.ear_latitude else "",
				"earthquake_ear_scale": earthquake.ear_scale if earthquake.ear_scale else "",
				"earthquake_ear_deep": earthquake.ear_deep if earthquake.ear_deep else "",
				"earthquake_ear_epicenter_pos":earthquake.ear_epicenter_pos if earthquake.ear_epicenter_pos else "",
			})
	return  HttpResponse(json.dumps(response_data), content_type="application/json")

	