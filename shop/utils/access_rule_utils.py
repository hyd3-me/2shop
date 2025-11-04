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
