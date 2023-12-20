from django.db import models
from library.models import Book, CustomUser  

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.title} - {self.user.username}"
