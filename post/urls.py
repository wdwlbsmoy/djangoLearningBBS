from django.urls import path,re_path
from post import views
from post.views import FirstView,SecondView
from django.urls import register_converter
from post.views import MonthConverter

register_converter(MonthConverter,'mth')

app_name = 'post'

urlpatterns = [
    path('hello_class/',FirstView.as_view()),
    path('second_class/',SecondView.as_view()),
    path('second_hello_class/',FirstView.as_view(html="Third：(%s) Hello Django BBS")),
    re_path('re_dynamic/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/',views.dynamic_hello),
    path('dynamic/<int:year>/<mth:month>/<int:day>/',views.dynamic_hello,name='dynamic_hello'),
    path('topic_list/',views.topic_list_view),
    path('topic/<int:topic_id>/',views.topic_detail_view),
    path('topic_comment/',views.add_comment_to_topic_view),
    path('dynamic_hello_reverse/',views.dynamic_hello_reverse),
    path('hello_redirect/',views.hello_redirect)
]