from django.contrib import admin
from post.models import Topic,Comment
from django.utils.translation import ugettext_lazy as _
# Register your models here.
# admin.site.register([Topic,Comment])
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    actions = ['topic_online','topic_offline']
    list_display = ['title','topic_content','topic_is_online','user']
    search_fields = ['^title','=user__username']
    list_per_page = 5
    list_max_show_all = 10
    raw_id_fields = ('user',)
    # list_filter = ['title','user__username']
    # ordering = ['id']
    # ordering = ['get_ordering']

    def save_model(self, request, obj, form, change):
        if change and 'is_online' in form.changed_data and not obj.is_online:
            self.message_user(request,'Topic(%s) 被管理员删除了' %obj.id)
            obj.title= '%s(%s)' %(obj.title,'管理员删除')
        super(TopicAdmin,self).save_model(request,obj,form,change)

    # def delete_model(self, request, obj):
    #     obj.is_online = False
    #     self.message_user(request,'Topic(%s) 被删除成功！' %obj.id)
    #     super(TopicAdmin,self).delete_model(request,obj)

    def get_ordering(self,request):
        if request.user.is_superuser:
            return ['id']
        else:
            return self.ordering

    class TitleFilter(admin.SimpleListFilter):
        title = _('标题过滤')
        parameter_name = 'tf'

        def lookups(self,request,model_admin):
            return (
                ('first',_('包含first')),('!first',_('不包含first')),
            )
        
        def queryset(self,request,queryset):
            if self.value() == 'first':
                return queryset.filter(title__contains = self.value())
            elif self.value() == '!first':
                return queryset.exclude(title__contains = self.value()[1:])
            else:
                return queryset

    list_filter = [TitleFilter,'user__username']


    def topic_is_online(self,obj):
        return '是' if obj.is_online else '否'
    topic_is_online.short_description = '话题是否在线'
    
    def topic_content(self,obj):
        return obj.content[:30]
    topic_content.short_description = '话题内容'

    def topic_online(self,request,queryset):
        rows_updated = queryset.update(is_online=True)
        self.message_user(request,'%s topic online' % rows_updated)
    topic_online.short_description = '上线所选的 %s' %Topic._meta.verbose_name

    def topic_offline(self,request,queryset):
        rows_update = queryset.update(is_online=False)
        self.message_user(request,'%s topic offline' % rows_update)
    topic_offline.short_description = '下线所选的 %s' %Topic._meta.verbose_name

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass