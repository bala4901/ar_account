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
from datetime import date, datetime, tzinfo
from openerp.tools.translate import _
import netsvc
import decimal_precision as dp


class internal_transfer(osv.osv):
    _name = 'account.internal_transfer'
    _description = 'Internal Transfer'
    _inherit = ['mail.thread']

    def default_name(self, cr, uid, context={}):
        return '/'

    def default_transfer_date(self, cr, uid, context={}):
        #TODO
        return True

    def default_company_id(self, cr, uid, context={}):
        #TODO
        return False

    def default_internal_transfer_account_id(self, cr, uid, context={}):
        #TODO
        return False

    def default_state(self, cr, uid, context={}):
        return 'draft'

    _columns =  {
                'name' : fields.char(string='# Transfer', size=30, required=True, readonly=True),
                'transfer_date' : fields.date(string='Transfer Date', required=True),
                'company_id' : fields.many2one(string='Company', obj='res.company', required=True),
                'source_journal_id' : fields.many2one(string='Source Journal', obj='account.journal', required=True),
                'destination_journal_id' : fields.many2one(string='Destination Journal', obj='account.journal', required=True),
                'internal_transfer_account_id' : fields.many2one(string='Internal Transfer Account', obj='account.account', required=True),
                'amount' : fields.float(string='Amount', digits_compute=dp.get_precision('Account'), required=True),
                'description' : fields.text(string='Description'),
                'state' : fields.selection([('draft','Draft'),('confirm','Waiting For Approval'),('approve','Ready To Process'),('done','Done'),('cancel','Cancel')], 'Status', readonly=True),
                'created_user_id' : fields.many2one(string='Created By', obj='res.users', readonly=True),
                'created_time' : fields.datetime(string='Created Time', readonly=True),
                'confirmed_time' : fields.datetime(string='Confirmed Time', readonly=True),
                'confirmed_user_id' : fields.many2one(string='Confirmed By', obj='res.users', readonly=True),                       
                'approved_time' : fields.datetime(string='Approved Time', readonly=True),
                'approved_user_id' : fields.many2one(string='Approved By', obj='res.users', readonly=True),     
                'processed_time' : fields.datetime(string='Processed Time', readonly=True),
                'processed_user_id' : fields.many2one(string='Process By', obj='res.users', readonly=True),             
                'cancelled_time' : fields.datetime(string='Cancelled Time', readonly=True),
                'cancelled_user_id' : fields.many2one(string='Cancelled By', obj='res.users', readonly=True),                                                                                               
                'cancelled_reason' : fields.text(string='Cancelled Reason', readonly=True),

                }

    _defaults = {
                'name' : default_name,
                'transfer_date' : default_transfer_date,
                'company_id' : default_company_id,
                'internal_transfer_account_id' : default_internal_transfer_account_id,
                'state' : default_state,
                }

    #========================================       
    # WORKFLOW METHOD
    #
    # Method yang dijalankan oleh workflow
    #========================================   
                
    def workflow_action_confirm(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.buat_sequence(cr, uid, id):
                return False
                
            if not self.log_audit(cr, uid, id, 'confirmed'):
                return False
                
        return True

    def workflow_action_approve(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit(cr, uid, id, 'approved'):
                return False
                
        return True
        
    def workflow_action_done(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit(cr, uid, id, 'processed'):
                return False
                
        return True     
        
    def workflow_action_cancel(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.log_audit(cr, uid, id, 'cancelled'):
                return False
                
        return True

    #============================================== 
    # BUTTON METHOD
    #
    # Method yang dijalankan oleh button dengan tipe object
    #==============================================
    
    def button_action_cancel(self, cr, uid, ids, context={}):
        wkf_service = netsvc.LocalService('workflow')
        
        for id in ids:
            if not self.delete_workflow_instance(cr, uid, id):
                return False
                
            if not self.create_workflow_instance(cr, uid, id):
                return False
                
            wkf_service.trg_validate(uid, 'account.internal_transfer', id, 'button_cancel', cr)

        return True
        
    def button_action_set_to_draft(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.delete_workflow_instance(cr, uid, id):
                return False
                
            if not self.create_workflow_instance(cr, uid, id):
                return False

            if not self.clear_log(cr, uid, id):
                return False

            if not self.log_audit(cr, uid, id, 'created'):
                return False
            
        return True             

    #============================================== 
    # OTHER METHOD
    #
    #==============================================
    
    def delete_workflow_instance(self, cr, uid, id):
        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_delete(uid, 'account.internal_transfer', id, cr)    
        
        return True
        
    def create_workflow_instance(self, cr, uid, id):
        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_create(uid, 'account.internal_transfer', id, cr)
        return True
        
    def clear_log(self, cr, uid, id):
        """
        Clear all the audit trial
        """
        
        val =   {
                    'created_user_id' : False,
                    'created_time' : False,     
                    'confirmed_user_id' : False,
                    'confirmed_time' : False,
                    'approved_user_id' : False,
                    'approved_time' : False,
                    'processed_user_id' : False,
                    'processed_time' : False,
                    'cancelled_user_id' : False,
                    'cancelled_time' : False,
                    }
                    
        self.write(cr, uid, [id], val)
        
        return True
        
    def log_audit(self, cr, uid, id, state):
        if state not in ['created','confirmed','approved','processed','cancelled']:
            raise osv.except_osv(_('Warning!'),_('Error on log_audit method'))
            return False
            
        state_dict =    {
                                    'created' : 'draft',
                                    'confirmed' : 'confirm',
                                    'approved' : 'approve',
                                    'processed' : 'done',
                                    'cancelled' : 'cancel'
                                    }
            
        val =   {
                    '%s_user_id' % (state) : uid ,
                    '%s_time' % (state) : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'state' : state_dict.get(state, False),
                    }
                    
        self.write(cr, uid, [id], val)
        
        return True

    def buat_sequence(self, cr, uid, id):
        obj_sequence = self.pool.get('ir.sequence')
        obj_user = self.pool.get('res.users')
        
        user = obj_user.browse(cr, uid, [uid])[0]

        internal_transfer = self.browse(cr, uid, [id])[0]

        if internal_transfer.name != '/':
            return True
        
        if not user.company_id.sequence_internal_transfer_id:
            raise osv.except_osv(_('Warning!'), _('Sequence for internal transfer is not configured'))
            return False

        sequence_id = user.company_id.sequence_internal_transfer_id.id      
        sequence = obj_sequence.next_by_id(cr, uid, sequence_id)
        
        self.write(cr, uid, [id], {'name' : sequence})
        
        return True         

    
internal_transfer()




