from django.db import models

class Posts(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название поста')
    url = models.URLField(max_length=300, verbose_name='Ссылка')
    created = models.DateTimeField(auto_now=True, verbose_name='Дата сохранения')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    def __str__(self):
        return str(self.title)