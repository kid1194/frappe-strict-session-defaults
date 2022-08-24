import frappe
from frappe.utils import has_common
from frappe.utils.data import now


_CACHE_KEY = "strict_session_defaults_settings"
_SETTINGS_DOCTYPE = "Strict Session Defaults Settings"
_LOG_DOCTYPE = "Strict Session Defaults Log"


def on_login(login_manager):
    if get_settings().is_enabled:
        user = frappe.session.user
        if not frappe.db.exists(_LOG_DOCTYPE, user):
            doc = frappe.db.get_doc({
                "doctype": _LOG_DOCTYPE,
                "user": user,
                "is_set": 0
            })
            doc.insert()


def on_logout(login_manager):
    frappe.delete_doc(_LOG_DOCTYPE, frappe.session.user)


@frappe.whitelist()
def get_settings() -> dict:
    user = frappe.session.user
    cache = frappe.cache().hget(_CACHE_KEY, user)
    
    if isinstance(cache, dict):
        return cache
    
    result = frappe._dict({
        "is_enabled": False,
    })
    
    settings = frappe.get_cached_doc(_SETTINGS_DOCTYPE)
    
    if not settings.is_enabled:
        frappe.cache().hset(_CACHE_KEY, user, result)
        return result
    
    users = [v.user for v in settings.users]
    if (
        (
            settings.users_condition == "Visible Only For Listed Users"
            and user not in users
        ) or (
            settings.users_condition == "Hidden Only From Listed Users"
            and user in users
        )
    ):
        frappe.cache().hset(_CACHE_KEY, user, result)
        return result
    
    roles = [v.role for v in settings.roles]
    if (
        (
            settings.roles_condition == "Visible Only For Listed Roles"
            and not has_common(roles, frappe.get_roles())
        ) or (
            settings.roles_condition == "Hidden Only From Listed Roles"
            and has_common(roles, frappe.get_roles())
        )
    ):
        frappe.cache().hset(_CACHE_KEY, user, result)
        return result
    
    result["is_enabled"] = True
    frappe.cache().hset(_CACHE_KEY, user, result)
    return result


@frappe.whitelist()
def get_status() -> dict:
    user = frappe.session.user
    result = {
        "is_ready": False,
        "show": False
    }
    
    if not frappe.cache().hget(_CACHE_KEY, user):
        return result
    
    result["is_ready"] = True
    
    if not get_settings().is_enabled:
        return result
    
    result["show"] = frappe.db.exists(_LOG_DOCTYPE, {
        "user": user,
        "is_set": 0
    })
    return result

@frappe.whitelist()
def update_status() -> bool:
    user = frappe.session.user
    if not get_settings().is_enabled:
        return False
    
    if frappe.db.exists(_LOG_DOCTYPE, user):
        frappe.db.set_value(_LOG_DOCTYPE, user, "is_set", 1)
    
    return True