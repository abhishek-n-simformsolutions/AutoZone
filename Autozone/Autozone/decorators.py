from django.contrib.auth.decorators import user_passes_test


def normal_user_required(view_func):

    actual_decorator = user_passes_test(
        lambda u:u.is_authenticated and not u.is_new_cardealer and not u.is_bank
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def bank_user_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and not u.is_new_cardealer and u.is_bank
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def new_cardealer_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_new_cardealer and not u.is_bank
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def unauthenticated_required(view_func=None):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
