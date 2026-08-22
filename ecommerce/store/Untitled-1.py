def test_category_list_caches(self):
    self.client.get("/categories/")
    self.assertIsNotNone(cache.get("category_list"))

def test_category_cache_invalidates_on_create(self):
    self.client.get("/categories/")
    Category.objects.create(name="New", slug="new")
    self.assertIsNone(cache.get("category_list"))