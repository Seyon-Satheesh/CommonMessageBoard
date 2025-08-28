from django.db import models

# User Model (represents each and every user of this app)
class User(models.Model):
    username = models.CharField(max_length=32)
    correct_passwords = models.JSONField()
    incorrect_passwords = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# Message Model (represents every message posted on the message board)
class Message(models.Model):
    title = models.CharField(max_length=32)
    message = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)