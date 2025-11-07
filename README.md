# Shop Authentication & Authorization System

## О проекте

Данный проект представляет собой **кастомную систему аутентификации и авторизации** для интернет-магазина, разработанную в рамках тестового задания. Основная цель - создание собственной системы управления доступом без использования стандартных решений "из коробки" Django.

### Ключевые требования задания

- Реализовать собственную систему аутентификации (не на базе встроенных средств Django)
- Разработать гибкую систему авторизации на основе ролей и правил доступа
- Создать модель данных для управления правами пользователей
- Обеспечить корректные HTTP статусы (401 для неаутентифицированных, 403 для недостаточных прав)
- Реализовать полный цикл работы с пользователем (регистрация, вход, выход, обновление, удаление)

---

## Кастомные реализации

### Пользовательская модель (User)

**Что заменено:**

- Стандартная `django.contrib.auth.models.User`
- Встроенная аутентификация Django

**Что реализовано:**

```python
# users/models.py
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Email как идентификатор
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()  # Кастомный менеджер пользователей

    USERNAME_FIELD = "email"  # Аутентификация по email вместо username
```

#### Особенности

- Email как уникальный идентификатор (без username)
- Кастомный UserManager для создания пользователей
- Сохранена совместимость с PermissionsMixin для будущего расширения
- Мягкое удаление через is_active=False

### Система аутентификации

**Что заменено:**

- django.contrib.auth.middleware.AuthenticationMiddleware
- Стандартная сессионная аутентификация
- DRF TokenAuthentication

**Что реализовано:**

```python
# users/authentication.py
class CustomJWTAuthentication(authentication.BaseAuthentication):
    keyword = "Token"
    
    def authenticate(self, request):
        # Кастомная логика проверки JWT токенов
        # Валидация срока действия и подписи токенов
        # Интеграция с кастомной моделью Token
```

#### Особенности

- Собственная реализация JWT без сторонних библиотек
- Поддержка стандартного формата Authorization: Token {jwt}
- Правильная обработка 401/403 ошибок
- Совместимость с DRF ecosystem

### Модель токенов

**Что заменено:**

- rest_framework.authtoken.models.Token

Что реализовано:

```python
# users/models.py
class Token(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, ...)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()  # Автогенерация ключа
        return super().save(*args, **kwargs)
```

###$ Особенности

- Совместимость с DRF Token форматом
- Автоматическая генерация ключей
- Интеграция с кастомной пользовательской моделью
- One-to-one связь с пользователем
