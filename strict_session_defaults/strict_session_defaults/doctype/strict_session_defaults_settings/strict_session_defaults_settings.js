/*
*  Strict Session Defaults © 2022
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to LICENSE file
*/


frappe.ui.form.on('Strict Session Defaults Settings', {
    setup: function(frm) {
        frm.get_field('visibility_note').html(`<p>
            The visibility of the <code>Session Defaults Popup</code> will be decided as follows:
            <ol>
                <li>
                    If the logged-in user is listed in the <code>Users</code> field then the value of <code>Hidden From Listed Users</code> will decide the visibility of the popup.
                </li>
                <li>
                    Else, If the logged-in user has any of the listed <code>Roles</code> field then the value of <code>Hidden From Listed Roles</code> will decide the visibility of the popup.
                </li>
            </ol>
        </p>`);
    }
});

frappe.ui.form.on('Strict Session Defaults Has Role', {
    role: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (!row.role) return;
        frm.doc.roles.forEach(function(r) {
            if (r.role === row.role) {
                frappe.msgprint({
                    title: __('Error'),
                    indicator: 'Red',
                    message: __(
                        'The role "{0}" already exist.',
                        [row.role]
                    ),
                });
                frappe.model.set_value(row, 'role', '');
            }
        });
    }
});

frappe.ui.form.on('Strict Session Defaults Has User', {
    user: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (!row.user) return;
        frm.doc.users.forEach(function(r) {
            if (r.user === row.user) {
                frappe.msgprint({
                    title: __('Error'),
                    indicator: 'Red',
                    message: __(
                        'The user "{0}" already exist.',
                        [row.user]
                    ),
                });
                frappe.model.set_value(row, 'user', '');
            }
        });
    }
});