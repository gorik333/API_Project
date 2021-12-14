from django.db import models


class UserIP(models.Model):
    ip = models.GenericIPAddressField(default='192.168.0.1')

    def __str__(self):
        return "IP: {0}".format(self.ip)


class UserRequest(models.Model):
    ip = models.ForeignKey(UserIP, on_delete=models.CASCADE, blank=True, null=True)

    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=64, blank=False)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return "{0}; User: {1} {2}".format(self.ip, self.first_name, self.last_name)

