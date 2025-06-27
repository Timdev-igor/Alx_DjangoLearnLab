from django.db import models

# ✅ One-to-Many: Department & Employees
class Department(models.Model):  
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

class Employee(models.Model):  
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.name

# ✅ One-to-One: Product & ProductDetail
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

class ProductDetail(models.Model):
    description = models.CharField(max_length=255)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="detail")

    class Meta:
        verbose_name = "Product Detail"
        verbose_name_plural = "Product Details"

    def __str__(self):
        return f"Details for {self.product.name}"

# ✅ Many-to-Many: Students & Courses
class Student(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name="courses")  

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name

# ✅ One-to-Many & Many-to-Many: Author, Books & Categories
class Author(models.Model):  
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books")  # ✅ Many-to-Many

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title
