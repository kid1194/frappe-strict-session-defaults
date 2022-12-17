# Frappe Strict Session Defaults

A small plugin for Frappe that enforces and manages the session defaults popup.

---

### Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
  - [Install](#install)
  - [Update](#update)
  - [Uninstall](#uninstall)
- [Usage](#usage)
- [Issues](#issues)
- [License](#license)

---

### Requirements
- Frappe >= v13.0.0

---

#### Setup

⚠️ *Important* ⚠️

*Do not forget to replace [sitename] with the name of your site in all commands.*

#### Install
1. Go to bench directory

```
cd ~/frappe-bench
```

2. Get plugin from Github

*(Required only once)*

```
bench get-app https://github.com/kid1194/frappe-strict-session-defaults
```

3. Build plugin

*(Required only once)*

```
bench build --app strict_session_defaults
```

4. Install plugin on a specific site

```
bench --site [sitename] install-app strict_session_defaults
```

5. Check the usage section below

#### Update
1. Go to app directory

```
cd ~/frappe-bench/apps/strict_session_defaults
```

2. Get updates from Github

```
git pull
```

3. Go to bench directory

```
cd ~/frappe-bench
```

4. Build plugin

```
bench build --app strict_session_defaults
```

5. Update a specific site

```
bench --site [sitename] migrate
```

6. (Optional) Restart bench

```
bench restart
```

#### Uninstall
1. Go to bench directory

```
cd ~/frappe-bench
```

2. Uninstall plugin from a specific site

```
bench --site [sitename] uninstall-app strict_session_defaults
```

3. Remove plugin from bench

```
bench remove-app strict_session_defaults
```

4. (Optional) Restart bench

```
bench restart
```

---

### Usage
1. Go to `Strict Session Defaults Settings`
2. Check `Is Enabled` box
3. Select the `Roles Condition` desired
4. Add the roles that the condition applies to
5. Handle the `Users Condition` and `Users` in the same way

---

### Issues
If you find bug in the plugin, please create a [bug report](https://github.com/kid1194/frappe-strict-session-defaults/issues/new?assignees=kid1194&labels=bug&title=%5BBUG%5D) and let us know about it.

---

### License
This repository has been released under the [MIT License](https://github.com/kid1194/frappe-strict-session-defaults/blob/main/LICENSE).
