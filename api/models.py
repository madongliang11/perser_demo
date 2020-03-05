from django.db import models


class UserGroup(models.Model):
    title = models.CharField(max_length=32)


class UserInfo(models.Model):
    user_type_choices = (
        (1, '普通用户'),
        (2, 'VIP用户'),
        (3, 'SVIP用户'),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    group = models.ForeignKey(to='UserGroup', on_delete=models.DO_NOTHING)
    roles = models.ManyToManyField('Role')


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class Role(models.Model):
    title = models.CharField(max_length=32)

