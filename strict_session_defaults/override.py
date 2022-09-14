# Frappe Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt

import json

import frappe
from frappe.utils import has_common, now


logger = frappe.logger("strict-session-defaults", file_count=50)


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
            "is_set": "0"
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
        log("Getting settings from cache", cache)
        return cache
    
    result = {
        "is_enabled": False,
        "reqd_fields": []
    }
    
    settings = frappe.get_cached_doc(_SETTINGS_DOCTYPE)
    
    if not settings.is_enabled:
        log("Plugin not enabled", settings.as_dict())
        frappe.cache().hset(_CACHE_KEY, user, result)
        return result
    
    is_visible = False
    
    users = [v.user for v in settings.users]
    log("Listed users in settings", users)
    if users:
        in_users = user in users
        hidden_from_users = settings.hidden_from_listed_users
        if (
            (not hidden_from_users and not in_users) or
            (hidden_from_users and in_users)
        ):
            log("Hidden from user", settings.as_dict())
            frappe.cache().hset(_CACHE_KEY, user, result)
            return result
        
        is_visible = True
    
    if not is_visible:
        roles = [v.role for v in settings.roles]
        log("Listed roles in settings", roles)
        if roles:
            in_roles = has_common(roles, frappe.get_roles())
            hidden_from_roles = settings.hidden_from_listed_roles
            if (
                (not hidden_from_roles and not in_roles) or
                (hidden_from_roles and in_roles)
            ):
                log("Hidden from roles", settings.as_dict())
                frappe.cache().hset(_CACHE_KEY, user, result)
                return result
    
    result["is_enabled"] = True
    
    if settings.reqd_fields:
        result["reqd_fields"] = list(set(settings.reqd_fields.split("\n")))
    
    log("Returned result", result)
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
        log("Status - Settings not ready", result)
        return result
    
    settings = get_settings()
    
    if not settings["is_enabled"]:
        log("Status - Settings not enabled", settings)
        return result
    
    result["show"] = True
    result["reqd_fields"] = settings["reqd_fields"]
    log("Status - Returned result", result)
    return result


@frappe.whitelist()
def update_status():
    user = frappe.session.user
    log = frappe.cache().hget(_LOG_KEY, user)
    
    if not log:
        return False
    
    doc = frappe.get_doc(_LOG_DOCTYPE, log)
    doc.is_set = "1"
    doc.save(ignore_permissions=True)
    frappe.cache().hdel(_LOG_KEY, user)
    
    return True


def clear_cache(user=None):
    if not user:
        user = frappe.session.user
    
    frappe.cache().hdel(_CACHE_KEY, user)
    frappe.cache().hdel(_LOG_KEY, user)


def log(msg, data):
    logger.debug({"message": msg, "data": data})