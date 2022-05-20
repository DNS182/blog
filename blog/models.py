from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=100 , unique = True)
    slug = models.SlugField(max_length= 100 ,blank =True)
    intro = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to= 'blog/'  )
    date_added = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.title + ' ' + ' ----> '+ self.user.username
    
    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post , self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 440 or img.width > 220:
            output_size = (440, 220)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 440 or img.width > 220:
    #         output_size = (440, 220)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    

class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , related_name='comments' , on_delete=models.CASCADE )
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.body[0:15]


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name + " has messaged " + self.subject
