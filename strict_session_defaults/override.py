# Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import frappe
from frappe import _dict
from frappe.utils import cint, has_common


_SETTINGS_DOCTYPE = "Strict Session Defaults Settings"
_LOG_DOCTYPE = "Strict Session Defaults Log"


def on_login(login_manager):
    user = login_manager.user
    settings = get_settings(user)
    if settings.enabled:
        log = frappe.get_doc({
            "doctype": _LOG_DOCTYPE,
            "user": user,
            "is_set": 0
        })
        log.insert(ignore_permissions=True)
        set_user_cache(_LOG_KEY, user, log.name)


def on_logout(login_manager):
    clear_user_cache(login_manager.user)


@frappe.whitelist()
def get_settings(user=None) -> dict:
    if not user:
        user = frappe.session.user
    
    cache = get_user_cache(_SETTINGS_DOCTYPE, user)
    if (
        isinstance(cache, dict) and "enabled" in cache and
        "reqd_fields" not in cache and "users_to_show" not in cache
    ):
        return _dict(cache)
    
    result = _dict({
        "enabled": False,
        "reqds": []
    })
    status = 0
    settings = frappe.get_cached_doc(_SETTINGS_DOCTYPE)
    
    if not cint(settings.enabled):
        status = 2
    
    if not status and settings.users:
        users = [v.user for v in settings.users]
        if users and user in users:
            status = 2 if settings.hidden_from_listed_users else 1
    
    if not status and settings.roles:
        roles = [v.role for v in settings.roles]
        if roles and has_common(roles, frappe.get_roles()):
            status = 2 if settings.hidden_from_listed_roles else 1
    
    if status == 1:
        result.enabled = True
        if settings.reqd_fields:
            result.reqds = list(set(settings.reqd_fields.split("\n")))
    
    set_user_cache(_CACHE_KEY, user, result)
    
    return result


@frappe.whitelist()
def get_status() -> dict:
    user = frappe.session.user
    result = _dict({
        "show": False,
        "reqds": []
    })
    
    if not user or not get_user_cache(_LOG_DOCTYPE, user):
        return result
    
    settings = get_settings()
    if settings.enabled:
        result.show = True
        result.reqds = settings.reqds
    
    return result


@frappe.whitelist()
def update_status():
    user = frappe.session.user
    log = get_user_cache(_LOG_DOCTYPE, user)
    
    if not user or not log:
        return 0
    
    frappe.db.set_value(_LOG_DOCTYPE, log, "is_set", 1)
    del_user_cache(_LOG_DOCTYPE, user)
    
    return 1


def get_user_cache(dt, user):
    if not user:
        user = frappe.session.user
    
    if user:
        return frappe.cache().hget(dt, user)
    
    return None


def set_user_cache(dt, user, data):
    frappe.cache().hset(dt, user, data)


def del_user_cache(dt, user=None):
    if not user:
        user = frappe.session.user
    
    if user:
        frappe.cache().hdel(dt, user)


def clear_user_cache(user=None):
    del_user_cache(_SETTINGS_DOCTYPE, user)
    del_user_cache(_LOG_DOCTYPE, user)


def clear_document_cache(dt, name=None):
    if name is None:
        name = dt
    
    frappe.clear_cache(doctype=dt)
    frappe.clear_document_cache(dt, name)
    frappe.cache().delete_key(dt)