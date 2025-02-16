# Retrieve the book
retrieved_book = Book.objects.get(title="1984")

# Print book details
print(retrieved_book.title, retrieved_book.author, retrieved_book.publication_year)
