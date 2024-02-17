from django.db import models

# Create your models here.
class Docs(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()

    def __str__(self):
        return self.subject