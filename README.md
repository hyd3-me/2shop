# Custom Authentication & Authorization System

This backend project implements a custom authentication and authorization system using Python, Django Rest Framework, and PostgreSQL. 

Key features include:
- User registration, login, logout, profile update, and soft deletion
- Role-based access control with fine-grained permissions
- Secure password storage with bcrypt
- Token-based authentication with JWT and/or session management
- API endpoints for user management and administrative control over access rules
- Mock views simulating business objects with proper access restrictions

The project focuses on designing a robust database schema and security mechanisms beyond default framework features, tailored for real-world access control scenarios.


Schema for Access Control Management
1. Пользователи и роли

    users: таблица с информацией о пользователях.

    roles: таблица ролей (например, администратор, менеджер, пользователь).

    Связь: users_roles — таблица many-to-many, связывает пользователя с ролями.

2. Объекты бизнес-логики (business objects)

    business_elements: таблица, описывающая объекты, к которым применяется доступ (например, категории, товары, заказы, пользователи).

    В таблице можно хранить основные метаданные: название, тип, уникальный ключ.

3. Правила доступа

    access_rules: таблица, описывающая правила доступа.

        role_id: ссылка на роль.

        element_id: ссылка на объект бизнес-логики.

        Права:

            read (bool)

            create (bool)

            update (bool)

            delete (bool)

        В контексте: может быть ограничение только для владения (например, пользователь может менять только свои заказы).

4. Реализация логики

    При каждом запросе API система определяет пользователя и его роли.

    Далее проверяет наличие соответствующих прав доступа к запрошенному ресурсу (объекту или его типу).

    В случае отсутствия прав — возвращается статус 403 (Forbidden).

    В случае, если пользователь не авторизован — 401 (Unauthorized).
