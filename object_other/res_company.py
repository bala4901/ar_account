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

class res_company(osv.osv):
    _name = 'res.company'
    _inherit = 'res.company'

    _columns =  {
                'account_writeoff_id' : fields.many2one(string='Default Write-Off Account', obj='account.account', domain=['|',('type','!=','view'),('type','!=','closed'),('type','!=','consolidation')]),
                'account_internal_transfer_id' : fields.many2one(string='Default Internal Transfer Account', obj='account.account'),
                'sequence_internal_transfer_id' : fields.many2one(string='Internal Transfer Sequence', obj='ir.sequence'),
                }
res_company()




