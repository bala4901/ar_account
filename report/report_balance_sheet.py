# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from report import report_sxw
from tools.translate import _
import pooler
from datetime import datetime

class report_balance_sheet(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_balance_sheet, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []

        company = self.pool.get('res.users').browse(self.cr, uid, uid, context=context).company_id
        header_report_name = ' - '.join((_('BALANCE SHEET'), company.name, company.currency_id.name))

        footer_date_time = self.formatLang(str(datetime.today()), date_time=True)

        self.localcontext.update({
            'report_name': _('Balance Sheet'),
            'isi_laporan' : self.lines,       
        })
        self.context = context        
        
    def lines(self, form):
        def _process_child(accounts, parent, level):
            # Cari akun yang akan diproses            
            account_rec = [acct for acct in accounts if acct['id'] == parent][0]    

            # Buat dict
            res =   {
                        'id' : account_rec['id'],
                        'type' : account_rec['type'],
                        'code' : account_rec['code'],
                        'name' : account_rec['name'],
                        'level' : level,
                        'debit' : account_rec['debit'],
                        'credit' : account_rec['credit'],
                        'balance' : abs(account_rec['balance']),
                        'parent_id' : account_rec['parent_id'],
                        }                                                     

            # Append res ke dalam result_acc
            self.isi_laporan.append(res)          

            # Jika akun mempunyai sub-akun, maka proses sub-akun
            if account_rec['child_id']:
                level += 1
                for child in account_rec['child_id']:
                    _process_child(accounts, child, level)
    
        obj_account_acoount = self.pool.get('account.account')
        obj_users = self.pool.get('res.users')
        
        ids = {}
        done = None
        level = 1
        user = obj_users.browse(self.cr, self.uid, [self.uid])[0]
              
        # Proses context untuk pencarian sub-akun
        ctx = {}
        ctx['date_from'] = self.get_from_date()
        ctx['date_to'] =  self.get_to_date()

        # Ambil default id dari neraca saldo
        akun_id = user.company_id.account_activa_id.id  
        ids = [akun_id]

        parents = ids
        
        # Ambil ids dari akun anak dari 'Neraca Saldo'        
        child_ids = obj_account_acoount._get_children_and_consol(self.cr, self.uid, ids, ctx)

        if child_ids:
            ids = child_ids

        # Ambil data account.account dari akun anak dari 'Neraca Saldo'
        account_fields = ['type', 'code', 'name', 'debit', 'credit', 'balance', 'parent_id', 'child_id']
        accounts = obj_account_acoount.read(self.cr, self.uid, ids, account_fields, ctx)

        # Gw ga tau nih fungsinya buat apa, wkwkwkwkwkwkwkwk        
        for parent in parents:
            level = 1
            _process_child(accounts, parent, level)

        return self.isi_laporan

    def get_from_date(self):
        return self.from_date
        
    def get_to_date(self):
        return self.to_date

report_sxw.report_sxw('report.report_balance_sheet', 'account.account', 'addons/ar_account/report/templates/account_report_balance_sheet.mako', parser=report_balance_sheet, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
