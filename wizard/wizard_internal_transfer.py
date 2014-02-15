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


from osv import osv,fields

class wizard_internal_transfer(osv.osv_memory):
    _name = 'account.wizard_internal_transfer'
    _description = 'Wizard Internal Transfer'

    def default_transit_account_id(self, cr, uid, context={}):
        #TODO:
        return False
    
    _columns =  {
                'transfer_date' : fields.date(string='Transfer Date', required=True),
                'source_journal_id' : fields.many2one(string='Source Journal', obj='account.journal', required=True),
                'source_currency_id' : fields.many2one(string='Source Currency', obj='res.currency', required=True),
                'destination_journal_id' : fields.many2one(string='Destination Journal', obj='account.journal', required=True),
                'destination_currency_id' : fields.many2one(string='Destination Currency', obj='res.currency', required=True),
                'exchange_rate' : fields.float(string='Exchange Rate', digits=(16,2)),
                'amount_transfer' : fields.float(string='Amount Transfer', digits=(16,2), required=True),
                'amount_receive' : fields.float(string='Amonut Receive', digits=(16,2), required=True),
                'description' : fields.char(string='Description', size=255, required=True),
                'transit_account_id' : fields.many2one(string='Transit Account', obj='account.account', required=True),
                'payment_method' : fields.selection(string='Payment Method', selection=[('bank_transfer','Bank Transfer'),('cheque','Cheque'),('giro','Giro')], readonly=False),
                'cheque_number' : fields.char(string='Cheque Number', size=50, readonly=False),
                'cheque_date' : fields.date(string='Cheque Date', readonly=False),
                'cheque_partner_bank_id' : fields.many2one(obj='res.partner.bank', string='Destination Bank Account', readonly=False),
                'cheque_bank_id' : fields.related('cheque_partner_bank_id', 'bank', type='many2one', relation='res.bank', string='Bank', store=False, readonly=True),
                'cheque_recepient' : fields.char(string='Cheque Recepient', size=100, readonly=False),
                }

    def onchange_source_journal_id(self, cr, uid, ids, source_journal_id):
        #TODO:
        value = {}
        domain = {}
        warning = {}

        return {'value' : value, 'domain' : domain, 'warning' : warning}

    def onchange_destination_journal_id(self, cr, uid, ids, destination_journal_id):
        #TODO:
        value = {}
        domain = {}
        warning = {}

        return {'value' : value, 'domain' : domain, 'warning' : warning}

    def button_recompute_amount_receive(self, cr, uid, ids, context={}):
        #TODO:
        for id in ids:
            pass

        return True

    def button_update_rate(self, cr, uid, ids, context={}):
        #TODO:
        for id in ids:
            pass

        return True

    def button_execute_wizard(self, cr, uid, ids, context={}):
        #TODO:
        for id in ids:
            pass

        return True

        
wizard_internal_transfer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

