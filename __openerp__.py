# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name' : 'AR - Accounting Application',
    'version' : '1.1',
    'author' : 'Andhitia Rama & Michael Viriyananda',
    'category' : 'Accounting',
    'summary' : 'Accounting Application',
    'description' : """
    """,
    'website': 'http://andhitiarama.wordpress.com',
    'images' : [],
    'depends' : ['ar_base', 'account_accountant', 'account_voucher'],
    'data' : [  'security/ir.model.access.csv',
                'security/data_GroupsBankPayment.xml',
                'security/data_GroupsBankReceipt.xml',
                'security/data_GroupsCashPayment.xml',
                'security/data_GroupsCashReceipt.xml',
                'security/data_GroupsMemorialJournal.xml',
                'data/data_VoucherType.xml',
                'view/view_BankPayment.xml',
                'window_action/waction_BankPayment.xml',
                'menu/menu_Account.xml',],
    'js' : [],
    'qweb' : [],
    'css' : [],
    'demo ': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application' : True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
