from django.db import models

# Create your models here.log2

# Author model represents an author with a name.
class Author(models.Model):
    name = models.CharField(max_length=100)# Stores the author's name.

    def __str__(self):
        return self.name
# Book model represents a book with a title, publication year, and a foreign key to Author.
class Book(models.Model):
    title = models.CharField(max_length=200)# Stores the book's title.
    publication_year = models.IntegerField() # Stores the year the book was published.
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)# Links to the Author model.

    def __str__(self):
        return self.title