from django import forms
from django.core.exceptions import ValidationError
from .models import Category, News


class CategoryForm(forms.Form):
    title = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'brandName',
            }
        )
    )

    def create(self):
        category = Category.objects.create(title=self.cleaned_data['title'])
        return category

    def update(self, category):
        category.title = self.cleaned_data['title']
        category.save()
        return category

class NewsForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'newsTitle',
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'newsContent',
                'rows': 5,
            }
        )
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'id': 'newsImage',
            }
        )
    )
    video_link = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'newsVideoLink',
            }
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'newsCategory',
            }
        )
    )

    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'video_link', 'category']

    def clean(self):
        cleaned_data = super().clean()
        video_link = cleaned_data.get('video_link')

        if video_link and not video_link.startswith('https://'):
            raise ValidationError("Video linki to'g'ri formatda bo'lishi kerak (https:// bilan boshlanishi kerak).")

        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image and self.instance.pk:
            return self.instance.image
        return image

    def update(self, news):
        news.title = self.cleaned_data.get('title')
        news.content = self.cleaned_data.get('content')
        news.image = self.cleaned_data.get('image')
        news.video_link = self.cleaned_data.get('video_link')
        news.category = self.cleaned_data.get('category')
        news.save()
        return news
