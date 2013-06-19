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

import tools
from osv import fields,osv
from decimal_precision import decimal_precision as dp


class report_account_payable(osv.osv):

    _name = 'account.report_account_payable'
    _description = 'Account Payable Report'
    _auto = False
    _columns = {
                            'name' : fields.char(string='# Invoice', size=100, readonly=True),
                            'partner_code' : fields.char(string='Supplier Code', size=30, readonly=True),
                            'partner_id' : fields.many2one(string='Supplier', obj='res.partner', readonly=True),
                            'date_invoice' : fields.date(string='Date Invoice', readonly=True),
                            'date_due' : fields.date(string='Date Due', readonly=True),
                            'amount_untaxed' : fields.float(string='Untaxed', digits_compute=dp.get_precision('Account'), readonly=True),
                            'amount_tax' : fields.float(string='Tax', digits_compute=dp.get_precision('Account'), readonly=True),
                            'amount_total' : fields.float(string='Total', digits_compute=dp.get_precision('Account'), readonly=True),
                            'amount_residual' : fields.float(string='Residual', digits_compute=dp.get_precision('Account'), readonly=True),
                            'aging' : fields.integer(string='Aging', readonly=True),
                            }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'account_report_account_payable')
        strSQL =    """
                            CREATE OR REPLACE view account_report_account_payable AS (
                                SELECT    
                                                    A.id AS id,
                                                    A.number AS name,
                                                    C.ref AS partner_code,
                                                    A.partner_id AS partner_id,
                                                    A.date_invoice AS date_invoice,
                                                    A.date_due AS date_due,
                                                    A.amount_untaxed AS amount_untaxed,
                                                    A.amount_tax AS amount_tax,
                                                    A.amount_total AS amount_total,
                                                    A.residual AS amount_residual,
                                                    A.aging AS aging
                                FROM    account_invoice AS A
                                JOIN account_invoice_type AS B ON A.invoice_type_id = B.id
                                JOIN res_partner AS C ON A.partner_id = C.id
                                WHERE    A.state = 'open' AND
                                                    B.name = 'Supplier Invoice'
                            )
                            """
        
        
        cr.execute(strSQL)

report_account_payable()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
