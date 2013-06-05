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
    'name': 'AR - Account',
    'version': '1.1',
    'author': 'Andhitia Rama & Michael Viriyananda',
    'category': 'Accounting',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    Modifikasi modul account
    """,
    'images': [],
    'depends': [    
                            'account_accountant', 
                            'account_voucher',
                            'ar_base_waktu',
                            'ar_base_sequence',
                            'ar_base_amount_to_text',
                            'ar_base'],
    'init_xml': [],
    'update_xml': [ 
                    'security/ir.model.access.csv',
                    'data/data_Sequence.xml',
                    'data/data_AccountJournal.xml',
                    'data/data_VoucherType.xml',
                    'ar_account_report.xml',
                    'wizard/wizard_import_move_line.xml',
                    'view/view_VoucherType.xml',
                    'view/view_MemorialJournal.xml',
                    'view/view_BankPayment.xml',
                    'view/view_BankReceipt.xml',
                    'view/view_CashPayment.xml',
                    'view/view_CashReceipt.xml',
                    'view/view_OtherBankPayment.xml',
                    'view/view_OtherBankReceipt.xml',
                    'view/view_OtherCashPayment.xml',
                    'view/view_OtherCashReceipt.xml',
                    'window_action/waction_VoucherType.xml',
                    'window_action/waction_MemorialJournal.xml',
                    'window_action/waction_BankPayment.xml',
                    'window_action/waction_BankReceipt.xml',
                    'window_action/waction_CashPayment.xml',
                    'window_action/waction_CashReceipt.xml',
                    'window_action/waction_OtherBankPayment.xml',
                    'window_action/waction_OtherBankReceipt.xml',
                    'window_action/waction_OtherCashPayment.xml',
                    'window_action/waction_OtherCashReceipt.xml',
                    'menu/menu_Account.xml',
                    'menu/menu_Setting.xml',
                    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
