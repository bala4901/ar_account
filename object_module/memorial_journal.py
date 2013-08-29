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
import netsvc

class memorial_journal(osv.osv):
    _name = 'account.memorial_journal'
    _inherit = 'account.voucher'
    _table = 'account_voucher'
    _description = 'Memorial Journal'

    def _workflow_trigger(self, cr, uid, ids, trigger, context=None):
        #override in order to trigger the workflow of account.voucher at the end of create, write and unlink operation
        #instead of it's own workflow (which is not existing)
        return self.pool.get('account.voucher')._workflow_trigger(cr, uid, ids, trigger, context=context)

    def _workflow_signal(self, cr, uid, ids, signal, context=None):
        #override in order to fire the workflow signal on given account.voucher workflow instance
        #instead of it's own workflow (which is not existing)
        return self.pool.get('account.voucher')._workflow_signal(cr, uid, ids, signal, context=context)
        


memorial_journal()




