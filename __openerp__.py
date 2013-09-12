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
                            'account_analytic_plans',
                            'account_cancel',
                            'ar_base_waktu',
                            'ar_base_sequence',
                            'ar_base_amount_to_text',
                            'ar_base'],
    'init_xml': [],
    'update_xml': [ 
                    'security/ir.model.access.csv',
                    'security/data_Application.xml',
                    'security/data_Groups.xml',
                    'data/data_Sequence.xml',
                    'data/data_AccountJournal.xml',
                    'data/data_VoucherType.xml',
                    'data/data_InvoiceType.xml',
                    'report/bank_payment.xml',
                    'report/cash_payment.xml',
                    'report/bank_receipt.xml',
                    'report/cash_receipt.xml',
                    'report/memorial_journal.xml',
                    'report/customer_invoice.xml',
                    'report/credit_note.xml',
                    'report/bank_cash_reconcilliation.xml',
                    'report/general_ledger.xml',
                    'report/report_account_receivable.xml',
                    'report/report_account_payable.xml',
                    'report/trial_balance.xml',
                    'report/balance_sheet.xml',
                    'report/equity_change.xml',
                    'report/statement.xml',
                    'workflow/workflow_AccountVoucher.xml',
                    'wizard/wizard_import_move_line.xml',
                    'wizard/wizard_post_voucher.xml',
                    'wizard/wizard_refund_invoice.xml',
                    'wizard/wizard_print_general_ledger.xml',
                    'wizard/wizard_print_trial_balance.xml',
                    #'wizard/wizard_print_balance_sheet.xml',
                     'wizard/wizard_print_profit_loss.xml',
                    'wizard/wizard_print_cash_flow.xml',
                    'wizard/wizard_print_equity_change.xml',
                    'wizard/wizard_cash_receipt.xml',
                    'wizard/wizard_bank_receipt.xml',
                    'wizard/wizard_cash_payment.xml',
                    'wizard/wizard_bank_payment.xml',
                    'wizard/wizard_print_statement.xml',
                    'view/view_VoucherType.xml',
                    'view/view_InvoiceType.xml',
                    'view/view_MemorialJournal.xml',
                    'view/view_BankPayment.xml',
                    'view/view_BankReceipt.xml',
                    'view/view_CashPayment.xml',
                    'view/view_CashReceipt.xml',
                    'view/view_OtherBankPayment.xml',
                    'view/view_OtherBankReceipt.xml',
                    'view/view_OtherCashPayment.xml',
                    'view/view_OtherCashReceipt.xml',
                    'view/view_CustomerInvoice.xml',
                    'view/view_SupplierInvoice.xml',
                    'view/view_CreditNote.xml',
                    'view/view_DebitNote.xml',
                    'view/view_ResCompany.xml',
                    'window_action/waction_VoucherType.xml',
                    'window_action/waction_InvoiceType.xml',
                    'window_action/waction_MemorialJournal.xml',
                    'window_action/waction_BankPayment.xml',
                    'window_action/waction_BankReceipt.xml',
                    'window_action/waction_CashPayment.xml',
                    'window_action/waction_CashReceipt.xml',
                    'window_action/waction_OtherBankPayment.xml',
                    'window_action/waction_OtherBankReceipt.xml',
                    'window_action/waction_OtherCashPayment.xml',
                    'window_action/waction_OtherCashReceipt.xml',
                    'window_action/waction_CustomerInvoice.xml',
                    'window_action/waction_SupplierInvoice.xml',
                    'window_action/waction_CreditNote.xml',
                    'window_action/waction_DebitNote.xml',
                    'board/board_AR.xml',
                    'board/board_AP.xml',
                    'board/board_Voucher.xml',
                    'menu/menu_Account.xml',
                    'menu/menu_Setting.xml',
                    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application':True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
