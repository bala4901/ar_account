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

class wizard_bank_payment(osv.osv_memory):
    _name = 'account.wizard_bank_payment'
    _description = 'Wizard Bank Payment'

    _columns = {
                'journal_id' : fields.many2one(string='Journal', obj='account.journal', required=True),
                'name' : fields.char(string='Description', size=100, required=True),
                'date':fields.date(string='Date', required=True),
                'payment_method' : fields.selection(string='Payment Method', selection=[('bank_transfer','Bank Transfer'),('cheque','Cheque'),('giro','Giro')], required=True),
                'cheque_number' : fields.char(string='Cheque Number', size=50, readonly=False),
                'cheque_date' : fields.date(string='Cheque Date', readonly=False),
                'cheque_partner_bank_id' : fields.many2one(obj='res.partner.bank', string='Destination Bank Account', readonly=False),
                'cheque_bank_id' : fields.related('cheque_partner_bank_id', 'bank', type='many2one', relation='res.bank', string='Bank', store=True, readonly=True),
                'cheque_recepient' : fields.char(string='Cheque Recepient', size=100, readonly=False),
                'cheque_is_giro' : fields.boolean('Is Giro?'),
                }

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        res = super(wizard_bank_payment, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        x = []
        mod_obj = self.pool.get('ir.model.data')
        obj_account_voucher_type = self.pool.get('account.voucher_type')
        if context is None: context = {}

        voucher_type = context.get('voucher_type')

        if voucher_type and view_type == 'form':

                kriteria = [('name','=',voucher_type)]
                voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)[0]

                voucher = obj_account_voucher_type.browse(cr, uid, voucher_type_ids, context=context)

                result = mod_obj.get_object_reference(cr, uid, voucher.modul_origin, voucher.model_view_form)
                result = result and result[1] or False
                view_id = result
                
                if voucher.allowed_journal_ids:
                        for journal in voucher.allowed_journal_ids:
                                x.append(journal.id)
                domain_journal = list(set(x))

                for field in res['fields']:
                    if field == 'journal_id':
                        res['fields'][field]['domain'] = [('id','in',domain_journal)]
        return res

    def view_init(self, cr, uid, fields_list, context=None):

        obj_account_invoice = self.pool.get('account.invoice')

        if context is None:
            context = {}
            
        res = super(wizard_bank_payment, self).view_init(cr, uid, fields_list, context=context)
        
        record_id = context and context.get('active_id', False)
        
        if record_id:

            invoice = obj_account_invoice.browse(cr, uid, record_id, context=context)

            if invoice.state != 'open' :
                raise osv.except_osv(_('Warning !'), _("You may only pay invoices that are Open !"))
        return res

    def get_total(self, cr, uid, context=None):
        obj_account_invoice = self.pool.get('account.invoice')
        record_id = context.get('active_ids')
        total = 0.00

        for data in record_id:
            invoice_id = obj_account_invoice.browse(cr, uid, data)
            total = total + invoice_id.residual
        
        return total
                            
    def bank_payment(self, cr, uid, ids, context=None):
        obj_account_bank_payment = self.pool.get('account.bank_payment')
        obj_account_voucher_line = self.pool.get('account.voucher.line')
        obj_account_move_line = self.pool.get('account.move.line')
        obj_account_invoice = self.pool.get('account.invoice')
        obj_account_journal = self.pool.get('account.journal')
        obj_account_voucher_type = self.pool.get('account.voucher_type')
        obj_account_period = self.pool.get('account.period')

        record_id = context.get('active_ids')

        wizard = self.read(cr, uid, ids[0], context=context)

        #raise osv.except_osv(_('Error !'), _('%s')%record_id[0])

        journal = obj_account_journal.browse(cr, uid, wizard['journal_id'][0])

        voucher_type_ids = obj_account_voucher_type.search(cr, uid, [('name','=','Bank Payment')])[0]

        voucher_type = obj_account_voucher_type.browse(cr, uid, voucher_type_ids)

        payment_method = wizard['payment_method'] if wizard['payment_method'] else False
        cheque_number = wizard['cheque_number'] if wizard['cheque_number'] else False
        cheque_date = wizard['cheque_date'] if wizard['cheque_date'] else False
        cheque_partner_bank_id = wizard['cheque_partner_bank_id'][0] if wizard['cheque_partner_bank_id'] else False
        cheque_bank_id = wizard['cheque_bank_id'][0] if wizard['cheque_bank_id'] else False
        cheque_recepient = wizard['cheque_recepient'] if wizard['cheque_recepient'] else False
        cheque_is_giro = wizard['cheque_is_giro'] if wizard['cheque_is_giro'] else False
        
        period_id = obj_account_period.find(cr, uid, wizard['date'], context)
        
        val_header = {
                        'journal_id' : wizard['journal_id'][0],
                        'name' : wizard['name'][0],
                        'date' : wizard['date'],
                        'account_id' : journal.default_debit_account_id.id,
                        'voucher_type_id' : voucher_type.id,
                        'type' : voucher_type.default_header_type,
                        'amount' : self.get_total(cr, uid, context),
                        'payment_method' : payment_method,
                        'cheque_number' : cheque_number,
                        'cheque_date' : cheque_date,
                        'cheque_partner_bank_id' : cheque_partner_bank_id,
                        'cheque_bank_id' : cheque_bank_id,
                        'cheque_recepient' : cheque_recepient,
                        'cheque_is_giro' : cheque_is_giro,
                        'period_id' : period_id[0],
                        }

        new_account_bank_payment_id = obj_account_bank_payment.create(cr, uid, val_header, context)

        for data in record_id:
            invoice_id = obj_account_invoice.browse(cr, uid, data)

            move_line_ids = obj_account_move_line.search(cr, uid, [('move_id','=',invoice_id.move_id.id)])

            for move_line in obj_account_move_line.browse(cr, uid, move_line_ids):
                if move_line.account_id.type == 'payable':
                    amount = obj_account_voucher_line.compute_amount(cr, uid, move_line.id, move_line.journal_id.id, move_line.currency_id.id)['amount']
                    val = {
                            'voucher_id' : new_account_bank_payment_id,
                            'account_id' : move_line.account_id.id,
                            'move_line_id' : move_line.id,
                            'name' : move_line.name,
                            'amount' : amount,
                            'type' : 'dr',
                            }
                    new_account_bank_payment_detail_id = obj_account_voucher_line.create(cr, uid, val, context)

        return  {
                        'res_id' : new_account_bank_payment_id,
                        'name' : 'Bank Payment',
                        'view_type' : 'form',
                        'view_mode' : 'form',
                        'res_model' : 'account.bank_payment', #TODO
                        'type' : 'ir.actions.act_window',
                        'context' : context,
                        }
        
wizard_bank_payment()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

