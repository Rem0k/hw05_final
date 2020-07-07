from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text']
        labels = {
            'group': 'Группа',
            'text': 'Сообщение'
        }
        help_texts = {
            'group': 'Выберите группу (необязательно)',
            'text': 'Напишите пост тут :)'
        }
