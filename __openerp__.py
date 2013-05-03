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
    'author': 'Andhitia Rama',
    'category': 'Andhitia Rama/Account',
    'complexity': 'easy',
    'website': 'http://andhitiarama.wordpress.com',
    'description': """
    Modul account
    """,
    'author': 'Andhitia Rama',
    'website': 'http://andhitiarama.wordpress.com',
    'images': [],
    'depends': ['account', 
                'account_voucher',
                'ar_base_waktu',
                'ar_base_sequence',
                'ar_base'],
    'init_xml': [],
    'update_xml': [ 'data/data_Sequence.xml',
                    'data/data_AccountJournal.xml',
                    'view/view_PerusahaanAccount.xml',
                    'view/view_Sequence.xml',
                    'view/view_TipeInvoice.xml',
                    'view/view_JurnalAkuntansi.xml',
                    'view/view_KodeAkun.xml',
                    'view/view_Pajak.xml',
                    'view/view_Periode.xml',
                    'view/view_TahunFiskal.xml',
                    'view/view_TipeAkun.xml',
                    'view/view_JournalVoucher.xml',
                    'view/view_InvoiceARDefault.xml',
                    'view/view_VoucherType.xml',
                    'view/view_MemorialJournal.xml',
                    'window_action/waction_PerusahaanAccount.xml',
                    'window_action/waction_TipeInvoice.xml',
                    'window_action/waction_Sequence.xml',
                    'window_action/waction_JurnalAkuntansi.xml',
                    'window_action/waction_KodeAkun.xml',
                    'window_action/waction_Periode.xml',
                    'window_action/waction_Pajak.xml',
                    'window_action/waction_TahunFiskal.xml',
                    'window_action/waction_TipeAkun.xml',
                    'window_action/waction_JournalVoucher.xml',
                    'window_action/waction_InvoiceARDefault.xml',
                    'window_action/waction_VoucherType.xml',
                    'window_action/waction_MemorialJournal.xml',
                    'menu/menu_Account.xml'],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
