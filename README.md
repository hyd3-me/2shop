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


Access Control System Design
Overview

This project implements a custom role-based access control (RBAC)

system designed to finely manage user permissions across various business resources within the API.

The system allows flexible, scalable control over who can read, create, update, or delete specific resources, with distinctions between accessing all objects or only those owned by the user.
Database Schema

    Roles
    Defines distinct user roles such as Administrator, Manager, User, and Guest. Each user can be assigned one or more roles.

    Business Elements
    Abstract representations of the business objects in the system (e.g., Users, Categories, Products, Orders, Cart). Each element denotes an API resource with access rules.

    Access Rules
    Link roles with business elements and define permissions using boolean flags for operations:

        read - Permission to read own objects.

        read_all - Permission to read all objects.

        create - Permission to create objects.

        update - Permission to update own objects.

        update_all - Permission to update all objects.

        delete - Permission to delete own objects.

        delete_all - Permission to delete all objects.

Interaction Workflow

    On each request, a custom middleware or permission class authenticates the user and collects their roles.

    The system then verifies if the user’s roles grant sufficient permissions for the requested resource and action.

    A response with HTTP 401 is returned if the user is unauthenticated.

    A response with HTTP 403 is returned if the user is authenticated but lacks the necessary permissions.

Integration with Project Models

    User accounts are linked with roles via a role assignment mechanism.

    Business elements correspond to the models already implemented such as Category, Product, Order, and Cart.

    Access logic is encapsulated in custom DRF permissions or middleware that enforce rules dynamically based on the database configuration.

Administration

    Administrative users have API endpoints to manage roles and access rules, allowing real-time configuration of permissions.

    The system supports adding new roles, defining new business elements, and updating access permissions without code changes.

Benefits

    Fine-grained, flexible access control suited for complex business requirements.

    Scalable architecture supports growth and new resource types.

    Clear separation of authentication and authorization concerns.

