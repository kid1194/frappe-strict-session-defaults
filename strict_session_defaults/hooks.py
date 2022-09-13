from . import __version__ as app_version
from frappe import __version__ as frappe_version

app_name = "strict_session_defaults"
app_title = "Strict Session Defaults"
app_publisher = "Ameen Ahmed (Level Up)"
app_description = "Frappe plugin that enforces and manages the session defaults popup."
app_icon = "octicon octicon-unlock"
app_color = "blue"
app_email = "kid1194@gmail.com"
app_license = "MIT"
is_frappe_above_v13 = int(frappe_version.split('.')[0]) > 13

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/strict_session_defaults/css/select.css"
# app_include_js = "/assets/strict_session_defaults/js/select.js"

app_include_js = ['strict_session_defaults.bundle.js'] if is_frappe_above_v13 else ['/assets/strict_session_defaults/js/strict_session_defaults.js']

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "strict_session_defaults/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "strict_session_defaults.utils.jinja_methods",
# 	"filters": "strict_session_defaults.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "strict_session_defaults.install.before_install"
after_install = "strict_session_defaults.setup.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "strict_session_defaults.notifications.get_notification_config"


# login
on_login = ["strict_session_defaults.override.on_login"]
on_logout = ["strict_session_defaults.override.on_logout"]
#on_session_creation = ["strict_session_defaults.override.on_session_creation"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"strict_session_defaults.tasks.all"
# 	],
# 	"daily": [
# 		"strict_session_defaults.tasks.daily"
# 	],
# 	"hourly": [
# 		"strict_session_defaults.tasks.hourly"
# 	],
# 	"weekly": [
# 		"strict_session_defaults.tasks.weekly"
# 	],
# 	"monthly": [
# 		"strict_session_defaults.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "strict_session_defaults.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "strict_session_defaults.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "strict_session_defaults.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"strict_session_defaults.auth.validate"
# ]

