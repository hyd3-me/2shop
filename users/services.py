def soft_delete_user(user):
    """
    Soft delete a user by setting is_active to False.
    Args:
        user (User): User instance to deactivate.
    """
    user.is_active = False
    user.save()
