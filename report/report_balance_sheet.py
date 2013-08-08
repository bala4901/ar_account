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
            'tanggal' : self.get_tanggal, 
        })
        self.context = context     

    def get_tanggal(self, data):
        tanggal = data['form']['to_date']

        month = tanggal[5:7]
        nama_bulan = ''
        tanggal_cnvt = ''
        
        bulan = {
                '01' : 'Januai',
                '02' : 'Pebruari',
                '03' : 'Maret',
                '04' : 'April',
                '05' : 'Mei',
                '06' : 'Juni',
                '07' : 'Juli',
                '08' : 'Agustus',
                '09' : 'September',
                '10' : 'Oktober',
                '11' : 'November',
                '12' : 'Desember'
                }

        nama_bulan = bulan.get(month, False)
        if not nama_bulan:
            return '-'
        
        tanggal_cnvt = tanggal[8:10] + ' ' + nama_bulan + ' ' + tanggal[:4]

        return tanggal

    def get_tanggal_tahun_selanjutnya(self, tanggal_tahun_selanjutnya):
        obj_fiscalyear = self.pool.get('account.fiscalyear')
        tanggal = tanggal_tahun_selanjutnya
        tahun = int(tanggal[:4]) - 1
        tanggal_periode_bulan = ''

        fiscalyear_ids = obj_fiscalyear.search(self.cr, self.uid, [('name', '=', str(tahun))])
        if fiscalyear_ids:
            fiscalyear = obj_fiscalyear.browse(self.cr, self.uid, fiscalyear_ids)[0]
            return fiscalyear.date_stop
        else:  
            return False

    def get_tanggal_tahun(self, tanggal_tahun):
        obj_fiscalyear = self.pool.get('account.fiscalyear')
        tanggal = tanggal_tahun
        tahun = tanggal[:4]
        tanggal_periode_bulan = ''

        fiscalyear_ids = obj_fiscalyear.search(self.cr, self.uid, [('name', '=', tahun)])
        if fiscalyear_ids:
            fiscalyear = obj_fiscalyear.browse(self.cr, self.uid, fiscalyear_ids)[0]
            return fiscalyear.date_start
        else:  
            return False

    def set_context(self, objects, data, ids, report_type=None):
        def _process_child(accounts, parent, level, akun_type):    
            account_rec = [acct for acct in accounts if acct['id'] == parent][0]  
            year_to_date = 0.00

            ctx_2 = {}
            ctx_2['date_to'] =  self.get_tanggal_tahun_selanjutnya(data['form']['to_date'])

            if ctx_2:
                account = self.pool.get('account.account').browse(self.cr, self.uid, account_rec['id'] , ctx_2)

                if account:
                    year_to_date = account.balance

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
                        'year_to_date' : year_to_date,
                        'akun_type' : akun_type
                        }                                                     

            objects.append(res)          

            if account_rec['child_id']:
                level += 1
                for child in account_rec['child_id']:
                    _process_child(accounts, child, level, akun_type)
    
        obj_account_acoount = self.pool.get('account.account')
        obj_users = self.pool.get('res.users')
        objects = []
        
        ids = {}
        done = None
        level = 1
        user = obj_users.browse(self.cr, self.uid, [self.uid])[0]
              
        ctx = {}
        ctx['date_to'] =  data['form']['to_date']
        ctx['date_from'] = self.get_tanggal_tahun(data['form']['to_date'])

        akun_activa_id = user.company_id.account_activa_id.id
        akun_pasiva_id = user.company_id.account_pasiva_id.id

        if akun_activa_id:
            ids = [akun_activa_id]
            akun_type = 'aktiva'

            parents = ids
                
            child_ids = obj_account_acoount._get_children_and_consol(self.cr, self.uid, ids, ctx)

            if child_ids:
                ids = child_ids

            account_fields = ['type', 'code', 'name', 'debit', 'credit', 'balance', 'parent_id', 'child_id']
            accounts = obj_account_acoount.read(self.cr, self.uid, ids, account_fields, ctx)
         
            for parent in parents:
                level = 1
                _process_child(accounts, parent, level, akun_type)

        if akun_pasiva_id:
            ids = [akun_pasiva_id]
            akun_type = 'pasiva'

            parents = ids
                
            child_ids = obj_account_acoount._get_children_and_consol(self.cr, self.uid, ids, ctx)

            if child_ids:
                ids = child_ids

            account_fields = ['type', 'code', 'name', 'debit', 'credit', 'balance', 'parent_id', 'child_id']
            accounts = obj_account_acoount.read(self.cr, self.uid, ids, account_fields, ctx)
         
            for parent in parents:
                level = 1
                _process_child(accounts, parent, level, akun_type)

        self.localcontext.update({
            'report_name': _('Balance Sheet'),   
            'tanggal' : self.get_tanggal, 
        })

        return super(report_balance_sheet, self).set_context(objects, data, ids,
                                                            report_type=report_type)

report_sxw.report_sxw('report.report_balance_sheet', 'account.account', 'addons/ar_account/report/templates/account_report_balance_sheet.mako', parser=report_balance_sheet, header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
