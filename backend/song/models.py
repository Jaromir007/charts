from django.db import models

# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length=255)
    chordspro_text = models.TextField()
    chordspro_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title