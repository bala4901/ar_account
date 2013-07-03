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

import xml
import copy
from operator import itemgetter
import time
import datetime
from report import report_sxw
import locale

class report_trial_balance(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_trial_balance, self).__init__(cr, uid, name, context=context)
        self.isi_laporan = []
        self.localcontext.update({
            'time': time,
            'isi_laporan' : self.lines,
			'locale':locale,            
        })
        self.context = context
        
    def set_context(self, objects, data, ids, report_type=None):
        obj_period = self.pool.get('account.period')
        self.to_date = data['form']['to_date']        
        
        period_ids = obj_period.find(self.cr, self.uid, self.to_date)
        
        if not period_ids:
            return super(report_trial_balance, self).set_context(objects, data, ids, report_type=report_type)           
            
        period = obj_period.browse(self.cr, self.uid, period_ids)[0]
        
        self.from_date =  period.fiscalyear_id.date_start        

        return super(report_trial_balance, self).set_context(objects, data, ids, report_type=report_type)           
        
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
        akun_id = user.company_id.account_root_id.id  
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
        

        

report_sxw.report_sxw('report.report_trial_balance', 'account.account', 'addons/ar_account/report/trial_balance.rml', parser=report_trial_balance, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
