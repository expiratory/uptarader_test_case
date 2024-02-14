from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name
