from django.db import models

class Author(models.Model):
  name = models.CharField(max_length=50)
  email = models.EmailField()

  def __str__(self):
      return self.name

class Article(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey('Author', related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return self.title