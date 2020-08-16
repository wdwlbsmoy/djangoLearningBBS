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
    path('topic/<int:topic_id>/',views.topic_detail_view,name='topic_detail'),
    path('topic_comment/',views.add_comment_to_topic_view),
    path('dynamic_hello_reverse/',views.dynamic_hello_reverse),
    # path('hello_redirect/',views.hello_redirect),
    path('index/',views.index_view),
    path('comment_up/<int:comment_id>',views.CommentUpRedirectView.as_view()),
    path('topics/',views.TopicList.as_view()),
    path('topic_view/<int:pk>/',views.TopicDetailView.as_view()),
    path('hello/',views.hello_django_bbs,name='hello'),
    path('search_topic_form/',views.search_topic_form),
    path('search_topic/',views.search_topic),
    path('topic_model_form/',views.topic_model_form)
]
