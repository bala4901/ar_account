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

class wizard_refund_invoice(osv.osv_memory):
    _name = 'account.wizard_refund_invoice'
    _description = 'Wizard Refund Invoice'
    
    _columns = {
                            'date_refund' : fields.date(string='Date Refund', required=True),
                            }
                            
    def button_refund_invoice(self, cr, uid, ids, context=None):
        obj_invoice = self.pool.get(context['active_model'])
        wizard = self.browse(cr, uid, ids)[0]
        
        invoice = obj_invoice.browse(cr, uid, context['active_ids'])[0]
        
        period_id = False
        description = 'Refund from %s' % (str(invoice.number))
        journal_id = invoice.invoice_type_id.refund_invoice_type_id and invoice.invoice_type_id.refund_invoice_type_id.id or False
        refund_id = obj_invoice.refund(cr, uid, [invoice.id], wizard.date_refund, period_id, description, journal_id)
        obj_invoice.button_compute(cr, uid, refund_id)
        
        return {}

        
        
                            

        
wizard_refund_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

