### API Usage

- **Filter books**:
  - By title (exact match): `/api/books/?title=Example`
  - By author (exact match): `/api/books/?author=John`
  - By publication year (exact match): `/api/books/?publication_year=2020`

- **Search books**:
  - By title or author: `/api/books/?search=Example`

- **Order books**:
  - By title (ascending): `/api/books/?ordering=title`
  - By publication year (descending): `/api/books/?ordering=-publication_year`