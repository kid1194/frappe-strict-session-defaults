# Frappe Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to license.txt

import frappe

def after_install():
    frappe.clear_cache()