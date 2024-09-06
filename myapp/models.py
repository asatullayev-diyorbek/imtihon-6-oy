from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Kategoriyalar'
        verbose_name = 'Kategoriya'


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    video_link  = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Yangiliklar'
        verbose_name = 'Yangilik'



