from django.db import models

class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Mission(models.Model):
    assigned_cat = models.OneToOneField(SpyCat, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission {self.id} - {'Completed' if self.is_completed else 'In Progress'}"


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
