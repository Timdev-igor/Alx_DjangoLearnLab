from rest_framework import serializers
from .models import Book, Author
# BookSerializer serializes all fields of the Book model and includes custom validation
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation to ensure the publication year is not in the future.
    def validate_publication_year(self, value):
        if value > 2025:  # current year 2025
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
# AuthorSerializer serializes the Author model and includes a nested BookSerializer.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)# Nested serializer for related book

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']