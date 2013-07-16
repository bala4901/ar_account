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

from lxml import etree

import netsvc
import time

from osv import osv,fields
from tools.translate import _
import decimal_precision as dp
from datetime import datetime, date

class wizard_print_statement(osv.osv_memory):
    _name = 'account.wizard_print_statement'
    _description = 'Wizard Print Statement'
    
    _columns = {
                            'company_id' : fields.many2one(string='Company', obj='res.company', required=True),
                            'partner_id' : fields.many2one(string='Customer', obj='res.partner', required=True, domain=[('customer','=', 1)] ),
                            'contact_partner_id' : fields.many2one(string='Customer Address', obj='res.partner.address', required=True),
                            'from_date' : fields.date(string='From Date', required=True),
                            'to_date' : fields.date(string='To Date', required=True),
                            }

    def onchange_partner_id(self, cr, uid, ids, partner_id):
        obj_partner = self.pool.get('res.partner')
        if not partner_id:
            return {'value': {'contact_partner_id': False}}

        address = obj_partner.address_get(cr, uid, [partner_id], ['contact'])['contact']

        val = {
            'contact_partner_id': address,
        }

        return {'value': val}
                            
    def button_print_report(self, cr, uid, ids, data, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        obj_account_invoice = self.pool.get('account.invoice')

        kriteria = [ ('partner_id','=',wizard.partner_id.id), ('date_invoice','>=',wizard.from_date + ' 00:00:00'), ('date_invoice','<=',wizard.to_date + ' 23:59:00'),('company_id','=',wizard.company_id.id)]

        invoice_ids = obj_account_invoice.search(cr, uid, kriteria)
        if invoice_ids:
            data['ids'] = invoice_ids
            data['model'] = 'account.invoice'
            data['output_type'] = 'pdf'
            val =   {
                        'from_date' : '%s 00:00:00' % (wizard.from_date),
                        'to_date' : '%s 23:59:00' % (wizard.to_date),
                        }
            data['variables'] = val
        return {'type': 'ir.actions.report.xml', 'report_name': 'account.report_statement', 'datas': data}
                          
wizard_print_statement()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

