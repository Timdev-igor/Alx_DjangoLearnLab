from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request): return HttpResponse("""
        <html>
            <head>
                <title>movie store</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    h1 { color: #2c3e50; }
                    p { font-size: 18px; }
                    .container { max-width: 600px; margin: auto; padding: 20px; border: 2px solid #2c3e50; border-radius: 10px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome to Andre&Clyde u dummy Store</h1>
                    <p>Explore our collection of amazing books, from fiction to self-improvement.</p>
                    <p><a href="#">Browse movies</a></p>
                </div>
            </body>
        </html>
    """)
