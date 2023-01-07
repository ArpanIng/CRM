from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    # each user can have only one user profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("agents:agent_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)  # Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads"
    )
    description = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("leads:lead_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


def post_user_created_signal(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
