from django import forms
from post.models import Topic
from django.core.exceptions import ValidationError

class TopicSearchForm(forms.Form):
    title = forms.CharField(label='Topic title',widget=forms.Textarea())

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("字符串长度太短！")
        return title

class TopicField(forms.Field):
    default_error_messages = {
        'invalid':'Enter a whole number.',
        'not_exist':'Model Not Exist',
    }

    def to_python(self, value):
        try:
            value = int(str(value).strip())
            return Topic.objects.get(pk=value)
        except (ValueError,TypeError):
            raise ValidationError(self.error_messages['invalid'],code='invalid')
        except Topic.DoesNotExist:
            raise ValidationError(self.error_messages['not_exist'],code='not_exist')

class SignField(forms.CharField):
    def clean(self, value):
        return 'django %s' %super().clean(value)

def even_validator(value):
    if value % 2 != 0:
        raise ValidationError('%d is not a even number' %value)

class EvenField(forms.IntegerField):
    def __init__(self,**kwargs):
        super().__init__(validators=[even_validator],**kwargs)

#ModelForm实现
from django.forms import widgets

class TopicModelForm(forms.ModelForm):
    class Meta:
        model = Topic
        labels = {'title':'标题','content':'内容'}
        help_texts = {'title':'简短的话题标题','content':'话题的详细内容'}
        widgets = {'content':widgets.Textarea(attrs={'cols':'60','rows':'5'})}
        field_classes = {'title':forms.EmailField}
        exclude = ('is_online','user')