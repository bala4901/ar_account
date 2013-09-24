##############################################################################
#
# Copyright (c) 2008-2011 Alistek Ltd (http://www.alistek.com) All Rights Reserved.
#                    General contacts <info@alistek.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This module is GPLv3 or newer and incompatible
# with OpenERP SA "AGPL + Private Use License"!
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from report import report_sxw
from report.report_sxw import rml_parse

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        ctx =   {
                'selected_company' : self.get_company,
                'statement_date' : self.get_statement_date,
                'date_from' : self.get_date_from,
                'date_to' : self.get_date_to,
                'partner' : self.get_partner,
                'contact' : self.get_contact,
                'currency' : self.get_currency,
                'bank' : self.get_bank,
                'invoice' : self.get_invoice,
                'user' : self.get_user,
                }
        self.localcontext.update(ctx)

    def set_context(self, objects, data, ids, report_type=None):
        self.company_id = data['form']['company_id'][0]
        self.statement_date = data['form']['statement_date']
        self.date_from = data['form']['date_from']
        self.date_to = data['form']['date_to']
        self.partner_id = data['form']['partner_id'][0]
        self.contact_id = data['form']['contact_id'][0]
        self.currency_id = data['form']['currency_id'][0]
        self.user_id = data['form']['user_id'][0]
        self.bank_id = data['form']['bank_id'][0]

        return super(Parser, self).set_context(objects, data, ids, report_type=report_type)

    def get_company(self):
        obj_company = self.pool.get('res.company')
        company = obj_company.browse(self.cr, self.uid, [self.company_id])[0]
        return company

    def get_statement_date(self):
        return self.statement_date

    def get_date_from(self):
        return self.date_from

    def get_date_to(self):
        return self.date_to

    def get_partner(self):
        obj_partner = self.pool.get('res.partner')

        partner = obj_partner.browse(self.cr, self.uid, [self.partner_id])[0]

        return partner

    def get_contact(self):
        obj_partner = self.pool.get('res.partner')

        partner = obj_partner.browse(self.cr, self.uid, [self.contact_id])[0]

        return partner

    def get_currency(self):
        obj_currency = self.pool.get('res.currency')

        currency = obj_currency.browse(self.cr, self.uid, [self.currency_id])[0]

        return currency

    def get_user(self):
        obj_user = self.pool.get('res.users')

        user = obj_user.browse(self.cr, self.uid, [self.user_id])[0]

        return user

    def get_bank(self):
        obj_bank = self.pool.get('res.partner.bank')

        bank = obj_bank.browse(self.cr, self.uid, [self.bank_id])[0]

        return bank

    def get_invoice(self):
        obj_invoice = self.pool.get('account.invoice')
        invoice = False

        criteria = [('type','=','out_invoice'),('company_id','=',self.company_id),('currency_id','=',self.currency_id),('state','=','open')]

        invoice_ids = obj_invoice.search(self.cr, self.uid, criteria)

        if invoice_ids:
            invoice = obj_invoice.browse(self.cr, self.uid, invoice_ids)

        return invoice





