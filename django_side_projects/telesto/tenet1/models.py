from django.db import models


# Create your models here.
class Author(models.Model):
    name= models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title= models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre =models.CharField(max_length=100 , 
        choices=[
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Sci-Fi', 'Science Fiction'),
    ] 
    )
    def __str__(self):
        return f"{self.title} by {self.author}  genre:{self.genre} price:{self.price}"
    
class Library(models.Model):
    title = models.CharField(max_length=100)
    books= models.ForeignKey(Book ,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} "
    #creating users//////////////////
# Custom User Manager
