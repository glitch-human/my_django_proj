from django.db import models

# Create your models here.
class MediaFile(models.Model):
    image = models.ImageField(upload_to='image/')
    audio = models.FileField(upload_to='audio/')

    def __str__(self):
        return f"Image: {self.image.name}, Audio: {self.audio.name}"