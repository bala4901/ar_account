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

import time
from datetime import datetime

from osv import osv,fields

class wizard_report_statement(osv.osv_memory):
    _name = 'account.wizard_report_statement'
    _description = 'Wizard Print Statement'

    def default_date_to(self, cr, uid, context={}):
        return datetime.now().strftime('%Y-%m-%d')

    def default_statement_date(self, cr, uid, context={}):
        return datetime.now().strftime('%Y-%m-%d')

    def default_user_id(self, cr, uid, context={}):
        return uid

    def default_company_id(self, cr, uid, context={}):
        obj_company = self.pool.get('res.company')

        company_id = obj_company._company_default_get(cr, uid, 'res.partner', context=context)

        return company_id

    _columns =  {
                'company_id' : fields.many2one(string='Company', obj='res.company', required=True),
                'partner_id' : fields.many2one(string='Customer', obj='res.partner', domain=[('customer','=',True)], required=True),
                'contact_id' : fields.many2one(string='Contact', obj='res.partner', required=True),
                'currency_id' : fields.many2one(string='Currency', obj='res.currency', required=True),
                'bank_id' : fields.many2one(string='Bank', obj='res.partner.bank', required=True),
                'date_from' : fields.date(string='Date From'),
                'date_to' : fields.date(string='Date To', required=True),
                'statement_date' : fields.date(string='Statement Date', required=True),
                'user_id' : fields.many2one(string='User', obj='res.users', required=True),
                }

    _defaults =     {
                    'company_id' : default_company_id,
                    'date_to' : default_date_to,
                    'statement_date' : default_statement_date,
                    'user_id' : default_user_id,
                    }

    def print_report(self, cr, uid, ids, context={}):
        if context is None:
            context = {}
        wizard = self.browse(cr, uid, ids)[0]
        datas = {'ids' : [wizard.company_id.id]}
        datas['model'] = 'res.company'

        datas['form'] = self.read(cr, uid, ids)[0]

        dict_return =   {
                        'type' : 'ir.actions.report.xml',
                        'report_name' : 'report_statement',
                        'datas' : datas,
                        }

        return dict_return
       
wizard_report_statement()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

