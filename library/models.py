from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name_plural = 'categories'
    
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/book/')
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.title
    
    def average_stars(self):
        reviews = self.review_set.all()
        if reviews:
            return sum(review.stars for review in reviews) / len(reviews)
        return 0
    

class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_returned = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    borrower = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.book.quantity -= 1
            self.book.save()
        elif self.is_returned:
            self.book.quantity += 1
            self.book.save()

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if not self.is_returned:
            self.book.quantity += 1
            self.book.save()

        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.book.title}"
