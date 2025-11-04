from shop.models import AccessRule


def create_access_rule(
    role,
    business_element,
    create_permission=False,
    read_permission=False,
    update_permission=False,
    delete_permission=False,
    can_create_for_other_users=False,
    read_all_permission=False,
    update_all_permission=False,
    delete_all_permission=False,
) -> AccessRule:
    if AccessRule.objects.filter(role=role, business_element=business_element).exists():
        raise ValueError(
            f"AccessRule for role {role} and element {business_element} already exists"
        )
    access_rule = AccessRule.objects.create(
        role=role,
        business_element=business_element,
        create_permission=create_permission,
        read_permission=read_permission,
        update_permission=update_permission,
        delete_permission=delete_permission,
        can_create_for_other_users=can_create_for_other_users,
        read_all_permission=read_all_permission,
        update_all_permission=update_all_permission,
        delete_all_permission=delete_all_permission,
    )
    return access_rule


def update_access_rule(
    role,
    business_element,
    create_permission=None,
    read_permission=None,
    update_permission=None,
    delete_permission=None,
    can_create_for_other_users=None,
    read_all_permission=None,
    update_all_permission=None,
    delete_all_permission=None,
):
    try:
        rule = AccessRule.objects.get(role=role, business_element=business_element)
    except AccessRule.DoesNotExist:
        raise ValueError(
            "AccessRule does not exist for the given role and business element"
        )

    if create_permission is not None:
        rule.create_permission = create_permission
    if read_permission is not None:
        rule.read_permission = read_permission
    if update_permission is not None:
        rule.update_permission = update_permission
    if delete_permission is not None:
        rule.delete_permission = delete_permission
    if can_create_for_other_users is not None:
        rule.can_create_for_other_users = can_create_for_other_users
    if read_all_permission is not None:
        rule.read_all_permission = read_all_permission
    if update_all_permission is not None:
        rule.update_all_permission = update_all_permission
    if delete_all_permission is not None:
        rule.delete_all_permission = delete_all_permission

    rule.save()
    return rule
