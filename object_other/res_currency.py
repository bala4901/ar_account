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


from osv import fields, osv

class res_currency(osv.osv):
    _name = 'res.currency'
    _inherit = 'res.currency'
    
    def _current_rate_silent(self, cr, uid, ids, name, arg, context=None):
        return self._current_rate_computation(cr, uid, ids, name, arg, False, context=context)

    _columns =  {
                'rounding': fields.float(string='Rounding Factor', digits=(12,12)),
                'rate_silent': fields.function(fnct=_current_rate_silent, string='Current Rate', digits=(12,12),
                    help='The rate of the currency to the currency of rate 1 (0 if no rate defined).'),
                }
res_currency()




