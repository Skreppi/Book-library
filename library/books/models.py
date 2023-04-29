from django.contrib.auth.models import User
from django.db import models


class Books(models.Model):
    title = models.CharField('Название', max_length=255)
    author = models.ForeignKey('Authors', on_delete=models.CASCADE, related_name='authors', verbose_name='Автор')
    description = models.TextField('Описание', blank=True, null=True)
    publication_date = models.DateField('Дата публикации', blank=True, null=True)


class Authors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
