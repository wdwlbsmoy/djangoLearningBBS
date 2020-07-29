from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls.converters import IntConverter
from post.models import Topic,Comment
from django.urls import reverse
from post.post_service import build_topic_base_info,build_topic_detail_info,add_comment_to_topic
from django.shortcuts import redirect

import time
def exec_time(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        res = func(*args,**kwargs)
        print('%ss elapsed for %s' %(time.time() - start, func.__name__))
        return res
    return wrapper

class ExecTimeMixin(object):
    @method_decorator(csrf_exempt)
    @method_decorator(exec_time)
    def dispatch(self,request,*args,**kwargs):
        return super(ExecTimeMixin,self).dispatch(request,*args,**kwargs)

class FirstView(ExecTimeMixin,View):
    html = '(%s) Hello Django BBS'

    def get(self,request):
        return HttpResponse(self.html % 'GET')

    def post(self,request):
        return HttpResponse(self.html % 'POST')


class SecondView(FirstView):
    html = 'Second: (%s) Hello Django BBS'

def dynamic_hello(request,year,month,day=15):
    html = "<h1>(%s) Hello Django BBS</h1>"
    return HttpResponse(html %('%s-%s-%s' % (year,month,day)))

class MonthConverter(IntConverter):
    regex = "0?[1-9]|1[0-2]"

def topic_list_view(request):
    '''
    话题列表
    :param request:
    :return:
    '''
    topic_qs = Topic.objects.all()
    result = {
        'count': topic_qs.count(),
        'info': [build_topic_base_info(topic) for topic in topic_qs]
    }
    return JsonResponse(result)

def topic_detail_view(request,topic_id):
    '''
    话题详细信息
    :param request:
    :param topic_id:
    :return:
    '''
    result = {}
    try:
        result = build_topic_detail_info(Topic.objects.get(pk=topic_id))
    except Topic.DoesNotExist:
        pass
    return JsonResponse(result)

@csrf_exempt
def add_comment_to_topic_view(request):
    '''
    给话题添加评论
    :param request:
    :return:
    '''
    topic_id = int(request.POST.get('id',0))
    content = request.POST.get('content','')
    topic = None

    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        pass
    if topic and content:
        return JsonResponse({'id': add_comment_to_topic(topic,content).id})
    return JsonResponse({})

def dynamic_hello_reverse(request):
    return HttpResponseRedirect(reverse('dynamic_hello',args=(2018,9,16),current_app=request.resolver_match.namespace))

def hello_redirect(request):
    return redirect('../topic_list/')
