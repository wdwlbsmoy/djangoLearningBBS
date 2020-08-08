from django import template

register = template.Library()

@register.simple_tag
def prefix_tag(cur_str):
    return 'Hello %s' % cur_str

@register.inclusion_tag('post/inclusion.html',takes_context=True)
def hello_inclusion_tag(context,cur_str):
    return {'hello':'%s %s' %(context['prefix'],cur_str)}