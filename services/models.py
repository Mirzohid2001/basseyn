from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    characteristics = models.TextField("Характеристики", blank=True)  # просто поле для текста
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="service_images/")
    alt_text = models.CharField(max_length=120, blank=True)

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_completed = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="project_images/")
    alt_text = models.CharField(max_length=120, blank=True)
