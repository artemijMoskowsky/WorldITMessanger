from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser


class WTUser(AbstractUser):
    # username = models.CharField(
    #     "Ім'я користувача",
    #     max_length = 150,
    #     unique = True,
    #     help_text = "Обов'язкове поле. Не більше ніж 150 символів. Тільки літери, цифри та @/./+/-/_.",
    #     error_messages = {
    #         'unique': "Користувач із таким ім'ям вже існує.",
    #     },
    # ) # Сносить при обновлении модели
    
    # email = models.EmailField('Email', unique=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    # class Meta:
    #     verbose_name = 'Користувач'
    #     verbose_name_plural = 'Користувачі'

    def __str__(self):
        return f"Name - {self.username}\n Email - {self.email}"