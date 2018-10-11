from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from decimal import Decimal

class User(models.Model):
	email = models.EmailField(max_length=200, unique=True)
	password = models.CharField(max_length=200)


class Account(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	user = models.ForeignKey('User', on_delete=models.CASCADE)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)


class Group(models.Model):
	name = models.CharField(max_length=200, unique=True)
	members = models.ManyToManyField('User', through='Membership', through_fields=('group', 'user'))

	def __str__(self):
		return self.name


class Membership(models.Model):
	group = models.ForeignKey('Group', on_delete=models.CASCADE)
	user = models.ForeignKey('User', on_delete=models.CASCADE)
	bank = models.ForeignKey('Card', on_delete=models.SET_NULL, blank=True, null=True)


class Card(models.Model):
	card_id = models.BigIntegerField(unique=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
	user = models.ForeignKey('User', on_delete=models.CASCADE)

	def __str__(self):
		return self.card_id


class Operation(models.Model):
	income = models.BooleanField()
	cost = models.DecimalField(max_digits=10, decimal_places=2)
	group_operation = models.BooleanField()
	date = models.DateTimeField(default=timezone.now)
	category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)


class Category(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name