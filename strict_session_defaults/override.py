# Frappe Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt

import json

import frappe
from frappe.utils import has_common


_CACHE_KEY = "strict_session_defaults_settings"
_SETTINGS_DOCTYPE = "Strict Session Defaults Settings"


def on_login(login_manager):
    user = login_manager.user
    clear_cache(user)
    settings = get_settings(user)
    if settings["is_enabled"]:
        if user not in settings["users_to_show"]:
            settings["users_to_show"].append(user)
            update_users_to_show(settings["users_to_show"])
            frappe.cache().hset(_CACHE_KEY, user, settings)
            log("Add user to show", settings)


def on_logout(login_manager):
    settings = get_settings()
    
    if settings["is_enabled"]:
        user = frappe.session.user
        if user in settings["users_to_show"]:
            idx = settings["users_to_show"].index(user)
            if idx >= 0:
                settings["users_to_show"].remove(idx)
                update_users_to_show(settings["users_to_show"])
                log("Remove user from show", settings)
    
    clear_cache()


@frappe.whitelist()
def get_settings(user=None) -> dict:
    if not user:
        user = frappe.session.user
    
    cache = frappe.cache().hget(_CACHE_KEY, user)
    
    if (
        isinstance(cache, dict) and "is_enabled" in cache and
        "reqd_fields" in cache and "users_to_show" in cache
    ):
        log("Getting settings from cache", cache)
        return cache
    
    result = {
        "is_enabled": False,
        "reqd_fields": [],
        "users_to_show": []
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
        visible_for_users = settings.users_condition == "Visible Only For Listed Users"
        if (
            (visible_for_users and not in_users) or
            (not visible_for_users and in_users)
        ):
            log("Hidden for user", settings.as_dict())
            frappe.cache().hset(_CACHE_KEY, user, result)
            return result
        
        is_visible = True
    
    if not is_visible:
        roles = [v.role for v in settings.roles]
        log("Listed roles in settings", roles)
        if roles:
            in_roles = has_common(roles, frappe.get_roles())
            visible_for_roles = settings.roles_condition == "Visible Only For Listed Roles"
            if (
                (visible_for_roles and not in_roles) or
                (not visible_for_roles and in_roles)
            ):
                log("Hidden for roles", settings.as_dict())
                frappe.cache().hset(_CACHE_KEY, user, result)
                return result
    
    result["is_enabled"] = True
    
    if settings.reqd_fields:
        result["reqd_fields"] = list(set(settings.reqd_fields.split("\n")))
    
    if settings.users_to_show:
        result["users_to_show"] = json.loads(settings.users_to_show)
    
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
    
    if not user or not frappe.cache().hget(_CACHE_KEY, user):
        log("Status - Settings not ready", result)
        return result
    
    settings = get_settings()
    
    if not settings["is_enabled"]:
        log("Status - Settings not enabled", settings)
        return result
    
    if user in settings["users_to_show"]:
        result["show"] = True
        log("Status - Show for user", result)
        idx = settings["users_to_show"].index(user)
        if idx >= 0:
            settings["users_to_show"].remove(idx)
            update_users_to_show(settings["users_to_show"])
            log("Status - Remove user from show", settings)
    
    result["reqd_fields"] = settings["reqd_fields"]
    
    clear_cache()
    log("Status - Returned result", result)
    return result


def update_users_to_show(data):
    settings = frappe.get_cached_doc(_SETTINGS_DOCTYPE)
    settings.users_to_show = json.dumps(data);
    settings.save(ignore_permissions=True)


def clear_cache(user=None):
    if not user:
        user = frappe.session.user
    
    frappe.cache().hdel(_CACHE_KEY, user)


def log(msg, data):
    if not isinstance(data, str):
        data = json.dumps(data)
    
    frappe.log_error("Strict Session Defaults", msg + ": " + data)