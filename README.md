# Frappe Strict Session Defaults
A small plugin for Frappe that enforces and manages the session defaults popup.

### Table of Contents
<ul>
    <li><a href="#requirements">Requirements</a></li>
    <li>
        <a href="#setup">Setup</a>
        <ul>
            <li><a href="#install">Install</a></li>
            <li><a href="#update">Update</a></li>
            <li><a href="#uninstall">Uninstall</a></li>
        </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
</ul>

---

### Requirements
- Frappe >= v13.0.0

---

### Setup

#### Install
1. Get the plugin from Github

*(Required only once)*

`bench get-app https://github.com/kid1194/frappe-strict-session-defaults`

2. Install the plugin on any instance/site you want

`bench --site [sitename] install-app strict_session_defaults`

3. Check the usage section below

#### Update
1. Go to the app directory (frappe-bench/apps/strict_session_defaults) and execute:

`git pull`

2. Go back to the frappe-bench directory and execute:

`bench --site [sitename] migrate`

3. *In case you need to restart bench, execute:*

`bench restart`

#### Uninstall
1. Uninstall the plugin from the instance/site

`bench --site [sitename] uninstall-app strict_session_defaults`

2. Uninstall the plugin from bench

`bench remove-app strict_session_defaults`

---

### Usage
1. Go to `Strict Session Defaults Settings`
2. Check `Is Enabled` box
3. Select the `Roles Condition` desired
4. Add the roles that the condition applies to
5. Handle the `Users Condition` and `Users` in the same way

---

### License
MIT
