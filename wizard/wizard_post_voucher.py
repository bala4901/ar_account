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

from osv import osv,fields

class wizard_post_voucher(osv.osv_memory):
    _name = 'account.wizard_post_voucher'
    _description = 'Wizard Post Voucher'
    
    _columns =  {
                'effective_date' : fields.date(string='Effective Date', required=True),
                }

                            
    def button_run_wizard(self, cr, uid, ids, context=None):
        obj_voucher = self.pool.get('account.voucher')
        obj_move = self.pool.get('account.move')
        obj_period = self.pool.get('account.period')

        wizard = self.browse(cr, uid, ids)[0]
        wkf_service = netsvc.LocalService('workflow')

        # find period
        period_ids = obj_period.find(cr, uid, wizard.effective_date)

        if not period_ids:
            raise osv.except_osv('Warning!', 'There is no period define for the effective date')
            return False
        else:
            period_id = period_ids[0]

        # raise osv.except_osv('a', str(context))
        voucher = obj_voucher.browse(cr, uid, context['active_ids'])[0]

        obj_voucher.write(cr, uid, [voucher.id], {'effective_date' : wizard.effective_date, 'period_id' : period_id})

        if voucher.state == 'ready':
            wkf_service.trg_validate(uid, 'account.voucher', voucher.id, 'button_proforma', cr)

        voucher = obj_voucher.browse(cr, uid, context['active_ids'])[0]

        obj_move.write(cr, uid, [voucher.move_id.id], {'date' : wizard.effective_date, 'period_id' : period_id})




        wkf_service.trg_validate(uid, 'account.voucher', voucher.id, 'button_posted', cr)

        return {}
        
        
                            

        
wizard_post_voucher()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

