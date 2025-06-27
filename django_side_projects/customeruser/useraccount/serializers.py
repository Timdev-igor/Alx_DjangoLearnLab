from rest_framework import serializers
from .models import Author, Book, Review
from datetime import date

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    """Extend BookSerializer to Include a Custom Field"""
    author = serializers.StringRelatedField()  # Shows author's name instead of ID
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source="author")
    reviews = ReviewSerializer(many=True, read_only=True)  # Nested Reviews
    days_since_creation = serializers.SerializerMethodField()  # Custom Field

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id', 'created_at']  # Ensuring 'id' and 'created_at' are not writable

    def validate(self, data):
        """Validate that the book title is at least 5 characters long."""
        if 'title' in data and len(data['title']) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return data

    def get_days_since_creation(self, obj):
        """Calculate the number of days since the book was created."""
        if obj.created_at:
            return (date.today() - obj.created_at.date()).days
        return None
