# Frappe Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt

import json

import frappe
from frappe.utils import cint, has_common, now


_CACHE_KEY = "strict_session_defaults_settings"
_LOG_KEY = "strict_session_defaults_log"
_SETTINGS_DOCTYPE = "Strict Session Defaults Settings"
_LOG_DOCTYPE = "Strict Session Defaults Log"


def on_login(login_manager):
    user = login_manager.user
    clear_cache(user)
    settings = get_settings(user)
    if settings["is_enabled"]:
        log = frappe.get_doc({
            "doctype": _LOG_DOCTYPE,
            "user": user,
            "is_set": 0
        })
        log.insert(ignore_permissions=True)
        frappe.cache().hset(_LOG_KEY, user, log.name)


def on_logout(login_manager):
    clear_cache()


@frappe.whitelist()
def get_settings(user=None) -> dict:
    if not user:
        user = frappe.session.user
    
    cache = frappe.cache().hget(_CACHE_KEY, user)
    
    if (
        isinstance(cache, dict) and "is_enabled" in cache and
        "reqd_fields" in cache and "users_to_show" not in cache
    ):
        return cache
    
    result = {
        "is_enabled": False,
        "reqd_fields": []
    }
    
    settings = frappe.get_cached_doc(_SETTINGS_DOCTYPE)
    
    if not settings.is_enabled:
        frappe.cache().hset(_CACHE_KEY, user, result)
        return result
    
    is_visible = False
    
    users = [v.user for v in settings.users]
    if users:
        in_users = user in users
        hidden_from_users = settings.hidden_from_listed_users == 1
        if (
            (not hidden_from_users and not in_users) or
            (hidden_from_users and in_users)
        ):
            frappe.cache().hset(_CACHE_KEY, user, result)
            return result
        
        is_visible = True
    
    if not is_visible:
        roles = [v.role for v in settings.roles]
        if roles:
            in_roles = has_common(roles, frappe.get_roles())
            hidden_from_roles = settings.hidden_from_listed_roles == 1
            if (
                (not hidden_from_roles and not in_roles) or
                (hidden_from_roles and in_roles)
            ):
                frappe.cache().hset(_CACHE_KEY, user, result)
                return result
    
    result["is_enabled"] = True
    
    if settings.reqd_fields:
        result["reqd_fields"] = list(set(settings.reqd_fields.split("\n")))
    
    frappe.cache().hset(_CACHE_KEY, user, result)
    return result


@frappe.whitelist()
def get_status() -> dict:
    user = frappe.session.user
    result = {
        "show": False,
        "reqd_fields": []
    }
    
    if not user or not frappe.cache().hget(_LOG_KEY, user):
        return result
    
    settings = get_settings()
    
    if settings["is_enabled"]:
        result["show"] = True
        result["reqd_fields"] = settings["reqd_fields"]
    
    return result


@frappe.whitelist()
def update_status():
    user = frappe.session.user
    log = frappe.cache().hget(_LOG_KEY, user)
    
    if not user or not log:
        return False
    
    frappe.db.set_value(_LOG_DOCTYPE, log, "is_set", 1)
    frappe.cache().hdel(_LOG_KEY, user)
    
    return True


def clear_cache(user=None):
    if not user:
        user = frappe.session.user
    
    if user:
        frappe.cache().hdel(_CACHE_KEY, user)
        frappe.cache().hdel(_LOG_KEY, user)