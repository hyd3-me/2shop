# Shop Authentication & Authorization System

## Суть проекта

**Кастомная система управления доступом** для интернет-магазина, реализующая:

- **Аутентификацию** - собственная JWT-реализация без стандартных средств Django  
- **Авторизацию** - гибкая ролевая модель с правилами доступа к бизнес-сущностям
- **Бизнес-логику** - базовые операции интернет-магазина (товары, категории, корзина, заказы)

## Как реализовано

### Аутентификация

- **Кастомная JWT-реализация** - собственная реализация
- **Stateless подход** - токены не хранятся в БД, проверяются через подпись
- **Формат `Token {jwt}`** - совместимость с DRF TokenAuthentication
- **Корректные HTTP-статусы** - 401 (неаутентифицирован), 403 (нет прав)

### Пользовательская модель

```python
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)  # Идентификатор вместо username
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    # Связь с ролями: user.roles.all()
```

## Система авторизации

### Архитектура разрешений

Система использует **несколько специализированных классов разрешений**, каждый для своей бизнес-сущности:

```python
# Разные permission классы для разных сущностей
CategoryViewSet -> AccessRulePermission
ProductViewSet -> AccessRulePermissionProduct  
OrderViewSet -> AccessRulePermissionOrder
AccessRuleViewSet -> IsAdminRolePermission
UserViewSet -> IsAdminRolePermission
```

### Специализированные классы разрешений

#### 1. Базовый паттерн для бизнес-сущностей

```python
class AccessRulePermission(BasePermission):
    def has_permission(self, request, view):
        # 1. Проверка аутентификации
        if not request.user.is_authenticated:
            return False
        
        # 2. Определение бизнес-элемента (хардкод в каждом классе)
        element_name = "Category"  # Уникально для каждого permission класса
        
        # 3. Поиск правил доступа для ролей пользователя
        user_roles = request.user.roles.all()
        element = BusinessElement.objects.get(name=element_name)
        
        # 4. Проверка прав для HTTP-метода
        if request.method == "GET":
            return any(rule.read_permission for rule in rules)
        elif request.method == "POST":
            return any(rule.create_permission for rule in rules)
        # ... и т.д. для PUT, PATCH, DELETE
```

#### 2. Конкретные реализации

**Для категорий** (`AccessRulePermission`):

- Простая проверка прав без дополнительной логики
- Все пользователи с `read_permission` могут просматривать категории
- Только администраторы/менеджеры с `create_permission` могут создавать

**Для товаров** (`AccessRulePermissionProduct`):

- Аналогична категориям, но для сущности "Product"

**Для заказов** (`AccessRulePermissionOrder`):

- **Сложная логика** с проверкой владельца
- `has_object_permission` для проверки прав на конкретный заказ
- Обычные пользователи видят только свои заказы
- Администраторы/менеджеры видят все заказы
- Дополнительная проверка `can_create_for_other_users`

**Для административных функций** (`IsAdminRolePermission`):

- Только пользователи с ролью "admin"
- Используется для управления правилами доступа и пользователями

### Пример работы в коде

```python
# views.py - назначение permission классов
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AccessRulePermission]  # Для категорий

class ProductViewSet(viewsets.ModelViewSet):  
    permission_classes = [AccessRulePermissionProduct]  # Для товаров

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AccessRulePermissionOrder]  # Для заказов
    
    def get_queryset(self):
        # Дополнительная фильтрация для заказов
        if user.roles.filter(name__in=["admin", "manager"]).exists():
            return Order.objects.all()  # Все заказы для админов
        return   Order.objects.filter(user=user) # Только свои заказы

class AccessRuleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRolePermission]  # Только админы
```

### Преимущества подхода

- ✅ **Изоляция** - каждый permission отвечает за свою сущность
- ✅ **Гибкость** - можно добавлять специфическую логику для каждой сущности
- ✅ **Простота тестирования** - каждый permission тестируется отдельно
- ✅ **Легкость поддержки** - изменения в одной сущности не затрагивают другие

## Тестирование системы

Система полностью покрыта тестами, проверяющими:

- ✅ Корректные права для разных ролей
- ✅ Правильные HTTP-статусы (401, 403, 200)
- ✅ Работу аутентификации (логин, логаут, регистрация)
- ✅ Бизнес-логику магазина

**Пример теста:**

```python
def test_admin_can_create_category(self):
    # Админ может создавать категории
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.post(self.url, data={"name": "Electronics"})
    self.assertEqual(response.status_code, 201)

def test_user_cannot_create_category(self):
    # Обычный пользователь не может создавать категории  
    self.client.force_authenticate(user=self.normal_user)
    response = self.client.post(self.url, data={"name": "Electronics"})
    self.assertEqual(response.status_code, 403)
```

### Текущее покрытие

```sh
Name                                                            Stmts   Miss  Cover
-----------------------------------------------------------------------------------
manage.py                                                          11      2    82%
shop/__init__.py                                                    0      0   100%
shop/admin.py                                                       1      1     0%
shop/apps.py                                                        4      0   100%
shop/migrations/0001_initial.py                                     5      0   100%
shop/migrations/0002_product.py                                     5      0   100%
shop/migrations/0003_order_orderitem.py                             6      0   100%
shop/migrations/0004_cart_cartitem.py                               6      0   100%
shop/migrations/0005_role.py                                        4      0   100%
shop/migrations/0006_businesselement_accessrule.py                  5      0   100%
shop/migrations/0007_accessrule_can_create_for_other_users.py       4      0   100%
shop/migrations/__init__.py                                         0      0   100%
shop/models.py                                                     54      3    94%
shop/permissions.py                                               174     47    73%
shop/serializers.py                                                65      3    95%
shop/tests/__init__.py                                              0      0   100%
shop/tests/test_access_control.py                                 305      2    99%
shop/tests/test_access_rule_permission.py                          48      0   100%
shop/tests/test_access_rule_utils.py                               52      0   100%
shop/tests/test_admin_accessrule_api.py                            67      0   100%
shop/tests/test_api.py                                             80      0   100%
shop/tests/test_jwt_utils.py                                       27      1    96%
shop/tests/test_models.py                                          16      0   100%
shop/tests/test_roles.py                                           11      0   100%
shop/urls.py                                                       12      0   100%
shop/utils/access_rule_utils.py                                    47      7    85%
shop/views.py                                                      67      5    93%
toshop/__init__.py                                                  0      0   100%
toshop/asgi.py                                                      4      4     0%
toshop/settings.py                                                 27      0   100%
toshop/tests/__init__.py                                            0      0   100%
toshop/tests/test_db_backend.py                                     7      0   100%
toshop/tests/test_db_connection.py                                 11      2    82%
toshop/tests/test_env_vars.py                                      10      0   100%
toshop/tests/test_logging.py                                        9      0   100%
toshop/tests/test_settings.py                                      12      0   100%
toshop/tests/tests.py                                               5      0   100%
toshop/urls.py                                                      3      0   100%
toshop/views.py                                                     3      0   100%
toshop/wsgi.py                                                      4      4     0%
users/__init__.py                                                   0      0   100%
users/admin.py                                                      1      1     0%
users/apps.py                                                       4      0   100%
users/authentication.py                                            47     15    68%
users/managers.py                                                  18      2    89%
users/migrations/0001_initial.py                                    5      0   100%
users/migrations/0002_user_roles.py                                 4      0   100%
users/migrations/0003_blacklistedtoken.py                           4      0   100%
users/migrations/0004_token.py                                      6      0   100%
users/migrations/__init__.py                                        0      0   100%
users/models.py                                                    14      1    93%
users/serializers.py                                               58      1    98%
users/services.py                                                   3      0   100%
users/tests/__init__.py                                             0      0   100%
users/tests/test_auth.py                                           35      0   100%
users/tests/test_password_change.py                                30      0   100%
users/tests/test_profile.py                                        21      0   100%
users/tests/test_registration.py                                   45      0   100%
users/tests/tests.py                                               37      0   100%
users/urls.py                                                       4      0   100%
users/utils/jwt_utils.py                                           10      0   100%
users/views.py                                                     46      0   100%
-----------------------------------------------------------------------------------
TOTAL                                                            1563    101    94%
```

## Быстрый старт

```bash
git clone https://github.com/hyd3-me/2shop.git source
python -m venv env
source env/bin/activate
cd source
python -m pip install -r requirements.txt 
python manage.py migrate
python manage.py test
```
