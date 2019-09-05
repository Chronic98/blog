from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.contrib.auth.models import User


def generate_file_name(instance, filename):
    filename = instance.slug + '.jpg'
    return '{0}/{1}'.format(instance, filename)


class Use(models.Model):
    SEX_CHOICES = [
        ('мужчина', 'мужчина'),
        ('женщина', 'женщина')
    ]
    MARITAL_STATUS_CHOICES = [
        ('не женат', 'не женат'),
        ('не замужем', 'не замужем'),
        ('женат', 'женат'),
        ('замужем', 'замужем')
    ]
    id_use = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    gender = models.CharField(max_length=8, choices=SEX_CHOICES)
    birthday = models.DateField()
    marital_status = models.CharField(
        max_length=11, choices=MARITAL_STATUS_CHOICES)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=10, unique=True)
    email = models.CharField(max_length=100)
    account = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    school = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to=generate_file_name)
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.id_use:
            self.slug = gen_slug(self.surname)
        super().save(*args, **kwargs)



def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']


