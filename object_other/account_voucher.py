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
from datetime import datetime
from tools.translate import _
import netsvc
import decimal_precision as dp

class account_voucher(osv.osv):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    _order = 'number'
    
    def default_journal_id(self, cr, uid, context={}):
        return False

    def default_voucher_type_id(self, cr, uid, context=None):
        obj_account_voucher_type = self.pool.get('account.voucher_type')
        voucher_type = []

        if context.get('voucher_type', False):
            kriteria = [('name', '=', context['voucher_type'])]

            voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)
            if voucher_type_ids : voucher_type = voucher_type_ids[0]

        return voucher_type

    def default_type(self, cr, uid, context=None):
        obj_account_voucher_type = self.pool.get('account.voucher_type')

        voucher_type_id = self.default_voucher_type_id(cr, uid, context)

        if not voucher_type_id : return False

        voucher_type = obj_account_voucher_type.browse(cr, uid, [voucher_type_id])[0]

        return voucher_type.default_header_type

    def default_created_user_id(self, cr, uid, context={}):
        return uid

    def default_created_time(self, cr, uid, context={}):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_amount_to_text(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        amount_to_text = []
        obj_account_voucher = self.pool.get('account.voucher')
        obj_res_currency = self.pool.get('res.currency')

        for account_voucher in obj_account_voucher.browse(cr, uid, ids):
            try:
                amount_to_text = obj_res_currency.terbilang(cr, uid, account_voucher.payment_rate_currency_id.id, account_voucher.amount) # INI CONTOH TERBILANG NYA
            except:
                amount_to_text = '-'
            res[account_voucher.id] = amount_to_text
        return res
        
    def default_payment_option(self, cr, uid, context={}):
        return 'with_writeoff'
        
    def default_writeoff_acc_id(self, cr, uid, context={}):
        obj_user = self.pool.get('res.users')
        
        user = obj_user.browse(cr, uid, [uid])[0]
        
        return user.company_id.account_writeoff_id and user.company_id.account_writeoff_id.id or False

    def function_amount_all(self, cr, uid, ids, name, args, context={}):
        res = {}
        for voucher in self.browse(cr, uid, ids):
            res[voucher.id] =   {
                                'total_cr' : 0.0,
                                'total_dr' : 0.0,
                                }
            if voucher.line_ids:
                for detail in voucher.line_ids:
                    if detail.type == 'dr' : res[voucher.id]['total_dr'] += detail.amount
                    if detail.type == 'cr' : res[voucher.id]['total_cr'] += detail.amount
        return res
        
    def _paid_amount_in_company_currency(self, cr, uid, ids, name, args, context=None):
        if context is None:
            context = {}
        res = {}
        ctx = context.copy()
        for v in self.browse(cr, uid, ids, context=context):
            ctx.update({'date': v.date})
            #make a new call to browse in order to have the right date in the context, to get the right currency rate
            voucher = self.browse(cr, uid, v.id, context=ctx)
            #ctx.update({
              #'voucher_special_currency': voucher.payment_rate_currency_id and voucher.payment_rate_currency_id.id or False,
              #'voucher_special_currency_rate': voucher.currency_id.rate * voucher.payment_rate,})

            res[voucher.id] =  self.pool.get('res.currency').compute(cr, uid, voucher.currency_id.id, voucher.company_id.currency_id.id, 1.0, context=ctx)
            res[voucher.id] = voucher.amount * res[voucher.id]
        return res

    _columns =  {
                                'voucher_type_id' : fields.many2one(obj='account.voucher_type', string='Voucher Type', readonly=True, states={'draft':[('readonly',False)]}),
                                'payment_method' : fields.selection(string='Payment Method', selection=[('bank_transfer','Bank Transfer'),('cheque','Cheque'),('giro','Giro')], readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_number' : fields.char(string='Cheque Number', size=50, readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_date' : fields.date(string='Cheque Date', readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_partner_bank_id' : fields.many2one(obj='res.partner.bank', string='Destination Bank Account', readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_bank_id' : fields.related('cheque_partner_bank_id', 'bank', type='many2one', relation='res.bank', string='Bank', store=True, readonly=True),
                                'cheque_recepient' : fields.char(string='Cheque Recepient', size=100, readonly=True, states={'draft':[('readonly',False)]}),
                                'cheque_is_giro' : fields.boolean('Is Giro?'),
                                'amount_to_text' : fields.function(fnct=get_amount_to_text, string='Terbilang', type='text', method=True, store=True),
                                'account_id':fields.many2one('account.account', 'Account', required=False, readonly=True, states={'draft':[('readonly',False)]}),
                                'total_dr' : fields.function(string='Total Debit', fnct=function_amount_all, type='float', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                                'total_cr' : fields.function(string='Total Credit', fnct=function_amount_all, type='float', digits_compute=dp.get_precision('Account'), method=True, store=True, multi='all'),
                                'paid_amount_in_company_currency': fields.function(_paid_amount_in_company_currency, string='Paid Amount in Company Currency', type='float', readonly=True),

                                'state' : fields.selection(selection=[('draft','Draft'),('confirm','Waiting For Approval'),('approve','Ready To Process'),('proforma','Pro-forma'),('posted','Posted'),('cancel','Cancelled')], string='State', readonly=True),
                                'created_time' : fields.datetime(string='Created Time', readonly=True),
                                'created_user_id' : fields.many2one(string='Created By', obj='res.users', readonly=True),
                                'confirmed_time' : fields.datetime(string='Confirmed Time', readonly=True),
                                'confirmed_user_id' : fields.many2one(string='Confirmed By', obj='res.users', readonly=True),                       
                                'approved_time' : fields.datetime(string='Approved Time', readonly=True),
                                'approved_user_id' : fields.many2one(string='Approved By', obj='res.users', readonly=True),     
                                'proforma_time' : fields.datetime(string='Proforma Time', readonly=True),
                                'proforma_user_id' : fields.many2one(string='Proforma By', obj='res.users', readonly=True),             
                                'posted_time' : fields.datetime(string='Posted Time', readonly=True),
                                'posted_user_id' : fields.many2one(string='Poested By', obj='res.users', readonly=True),             
                                'cancelled_time' : fields.datetime(string='Processed Time', readonly=True),
                                'cancelled_user_id' : fields.many2one(string='Process By', obj='res.users', readonly=True),                                                                                             
                                'cancelled_reason' : fields.text(string='Cancelled Reason', readonly=True),                                
                        }

    _defaults = {
                        'voucher_type_id' : default_voucher_type_id,
                        'type' : default_type,
                        'journal_id' : default_journal_id,
                        'payment_option' : default_payment_option,
                        'writeoff_acc_id' : default_writeoff_acc_id,
                        'created_user_id' : default_created_user_id,
                        'created_time' : default_created_time,
                        }

                                
                        
    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        res = super(account_voucher, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        x = []
        mod_obj = self.pool.get('ir.model.data')
        obj_account_voucher_type = self.pool.get('account.voucher_type')
        if context is None: context = {}
                
        voucher_type = context.get('voucher_type')

        if voucher_type and view_type == 'form':

            # raise osv.except_osv('a','a')
            kriteria = [('name','=',voucher_type)]
            voucher_type_ids = obj_account_voucher_type.search(cr, uid, kriteria)[0]

            voucher = obj_account_voucher_type.browse(cr, uid, voucher_type_ids, context=context)

            result = mod_obj.get_object_reference(cr, uid, voucher.modul_origin, voucher.model_view_form)
            result = result and result[1] or False
            view_id = result

            # SET journal_id DOMAIN SO IF ALLOWED JOURNAL IS FALSE
            res['fields']['journal_id']['domain'] = [('id','=',0)]
                        
            if voucher.allowed_journal_ids:
                for journal in voucher.allowed_journal_ids:
                    x.append(journal.id)
                    domain_journal = list(set(x))

                    for field in res['fields']:
                        if field == 'journal_id':
                            res['fields'][field]['domain'] = [('id','in',domain_journal)]
        return res
                        
    def first_move_line_get(self, cr, uid, voucher_id, move_id, company_currency, current_currency, context=None):
        '''
        Override untuk menyesuaikan field yang berkaitan dengan cek/giro
        '''
        voucher = self.browse(cr, uid, [voucher_id])[0]

        res =   {
                'payment_method' : voucher.payment_method,
                'cheque_number' : voucher.cheque_number,
                'cheque_date' : voucher.cheque_date,
                'cheque_partner_bank_id' : voucher.cheque_partner_bank_id.id,
                'cheque_recepient' : voucher.cheque_recepient
                }

        move_line = super(account_voucher, self).first_move_line_get(cr, uid, voucher_id, move_id, company_currency, current_currency)

        move_line.update(res)

        return move_line
        
    def workflow_action_confirm(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika confirm
        
        """
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'confirmed'):
                return False

        return True
    
    def workflow_action_approve(self, cr, uid, ids, context={}):
        """
        
        """ 
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'approved'):
                return False

        return True 
        
    def workflow_action_proforma(self, cr, uid, ids, context={}):
        """
        """
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'proforma'):
                return False

            if not self.proforma_voucher(cr, uid, [id]):
                return False

        return True         
    
    
    def workflow_action_posted(self, cr, uid, ids, context={}):
        """
        """ 
        for id in ids:              
            if not self.log_audit_trail(cr, uid, id, 'posted'):
                return False

            if not self.post_journal_entry(cr, uid, id):
                return False
                        
        return True     
    
    def workflow_action_cancel(self, cr, uid, ids, context={}):
        """
        Method yang dijalankan ketika cancel
        
        * Merubah state
        """ 
        for id in ids:
            if not self.log_audit_trail(cr, uid, id, 'cancelled'):
                return False

            if not self.cancel_account_voucher(cr, uid, id):
                return False
                
        return True     

    def button_action_cancel(self, cr, uid, ids, context={}):
        wkf_service = netsvc.LocalService('workflow')
        for id in ids:
            if not self.delete_workflow_instance(cr, uid, id):
                return False

            if not self.create_workflow_instance(cr, uid, id):
                return True

            wkf_service.trg_validate(uid, 'account.voucher', id, 'button_cancel', cr)

        return True

    def button_action_set_to_draft(self, cr, uid, ids, context={}):
        for id in ids:
            if not self.delete_workflow_instance(cr, uid, id):
                return False

            if not self.create_workflow_instance(cr, uid, id):
                return False

            if not self.clear_log_audit(cr, uid, id):
                return False

            if not self.log_audit_trail(cr, uid, id, 'created'):
                return False

        return True
        
        
    def log_audit_trail(self, cr, uid, id, state):
        if state not in ['created','confirmed','approved','proforma','posted','cancelled']:
            raise osv.except_osv(_('Peringatan!'),_('Error pada method log_audit'))
            return False
            
        state_dict =    {
                        'created' : 'draft',
                        'confirmed' : 'confirm',
                        'approved' : 'approve',
                        'proforma' : 'proforma',
                        'posted' : 'posted',
                        'cancelled' : 'cancel'
                        }
                
        val =   {
                '%s_user_id' % (state) : uid ,
                '%s_time' % (state) : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'state' : state_dict.get(state, False),
                }          
        self.write(cr, uid, [id], val)
        return True
        
    def clear_log_audit(self, cr, uid, id):
        val =   {
                'created_user_id' : False,
                'created_time' : False,     
                'confirmed_user_id' : False,
                'confirmed_time' : False,
                'approved_user_id' : False,
                'approved_time' : False,
                'proforma_user_id' : False,
                'proforma_time' : False,
                'posted_user_id' : False,
                'posted_time' : False,
                'cancelled_user_id' : False,
                'cancelled_time' : False,
                }
            
        self.write(cr, uid, [id], val)

        return True      
        
    def write_cancel_description(self, cr, uid, id, reason):
        self.write(cr, uid, [id], {'cancelled_reason' : reason})
        return True                 


    def create_workflow_instance(self, cr, uid, id):
        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_create(uid, 'account.voucher', id, cr)
        return True

    def delete_workflow_instance(self, cr, uid, id):
        wkf_service = netsvc.LocalService('workflow')
        wkf_service.trg_delete(uid, 'account.voucher', id, cr)
        return True

    def post_journal_entry(self, cr, uid, id):
        obj_move = self.pool.get('account.move')
         
        voucher = self.browse(cr, uid, [id])[0]
        
        if not voucher.move_id:
            if not self.proforma_voucher(cr, uid, [id]):
                return False
        
        voucher = self.browse(cr, uid, [id])[0]
        obj_move.post(cr, uid, [voucher.move_id.id], context={})            
        
        return True
        
       
    def cancel_account_voucher(self, cr, uid, id, context=None):

        obj_reconcile = self.pool.get('account.move.reconcile')
        obj_move = self.pool.get('account.move')
        obj_move_line = self.pool.get('account.move.line')
    
        voucher = self.browse(cr, uid, [id], context)[0]
    
        # Batalkan rekonsiliasi setiap voucher line
        for line in voucher.move_ids:
            if line.reconcile_id:
                move_lines = [move_line.id for move_line in line.reconcile_id.line_id]
                move_lines.remove(line.id)
                obj_reconcile.unlink(cr, uid, [line.reconcile_id.id])
                if len(move_lines) >= 2:
                    obj_move_line.reconcile_partial(cr, uid, move_lines, 'auto',context=context)
                    
        # Hapus account.move
        if voucher.move_id:
            obj_move.button_cancel(cr, uid, [voucher.move_id.id])
            obj_move.unlink(cr, uid, [voucher.move_id.id])
            
        res =   {
                'move_id' : False,
                }
                
        self.write(cr, uid, [id], res)
    
        return True
        
        
        
    def check_total_voucher(self, cr, uid, id):
        """
        Method untuk melakukan pengecekan agar total voucher == sum amount semua voucher line
        """
        
        voucher = self.browse(cr, uid, [id])[0]
        
        total = 0.0
        if voucher.line_ids:
            for line in voucher.line_ids:
                total += line.amount
                
        if voucher.amount == total and voucher.voucher_type_id.check_total:
            return True
        elif voucher.amount != total and voucher.voucher_type_id.check_total:
            return False
        else:
            return True
            
        
    def onchange_journal_id(self, cr, uid, ids, journal_id):
        value = {}
        domain = {}
        warning = {}
        
        obj_journal = self.pool.get('account.journal')
                
        if journal_id:
            journal = obj_journal.browse(cr, uid, [journal_id])[0]
            value['account_id'] = journal.default_debit_account_id.id
        
        
        return {'value' : value, 'domain' : domain, 'warning' : warning}
        
        
    def action_move_line_create(self, cr, uid, ids, context=None):
        '''
        Confirm the vouchers given in ids and create the journal entries for each of them
        '''
        if context is None:
            context = {}
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        for voucher in self.browse(cr, uid, ids, context=context):
            if voucher.move_id:
                continue
                
            line_total = 0.0

            company_currency = self._get_company_currency(cr, uid, voucher.id, context)
            current_currency = self._get_current_currency(cr, uid, voucher.id, context)
            # we select the context to use accordingly if it's a multicurrency case or not
            context = self._sel_context(cr, uid, voucher.id, context)
            # But for the operations made by _convert_amount, we always need to give the date in the context
            ctx = context.copy()
            ctx.update({'date': voucher.date})
            # Create the account move record.
            move_id = move_pool.create(cr, uid, self.account_move_get(cr, uid, voucher.id, context=context), context=context)
            # Get the name of the account_move just created
            name = move_pool.browse(cr, uid, move_id, context=context).name
        
            # Create the first line of the voucher
            # override untuk mengatasi voucher yang tidak ada header
            if voucher.account_id:
                move_line_id = move_line_pool.create(cr, uid, self.first_move_line_get(cr,uid,voucher.id, move_id, company_currency, current_currency, context), context)
                move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
                #line_total = move_line_brw.debit - move_line_brw.credit
                line_total = 0.0
        
            rec_list_ids = []
            #if voucher.type == 'sale':
                #line_total = line_total - self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
            #elif voucher.type == 'purchase':
                #line_total = line_total + self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)

            line_total = voucher.amount



            # Create one move line per voucher line where amount is not 0.0
            line_total, rec_list_ids = self.voucher_move_line_create(cr, uid, voucher.id, line_total, move_id, company_currency, current_currency, context)

            #Create the writeoff line if needed
            ml_writeoff = self.writeoff_move_line_get(cr, uid, voucher.id, line_total, move_id, name, company_currency, current_currency, False, context)
            if ml_writeoff:
                move_line_pool.create(cr, uid, ml_writeoff, context)


            # We post the voucher.
            self.write(cr, uid, [voucher.id], {
                'move_id': move_id,
                'number': name,
            })

            # We automatically reconcile the account move lines.
            #for rec_ids in rec_list_ids:
                #if len(rec_ids) >= 2:
                    #move_line_pool.reconcile_partial(cr, uid, rec_ids, writeoff_acc_id=False, writeoff_period_id=False, writeoff_journal_id=False)
        return True
        
    def voucher_move_line_create(self, cr, uid, voucher_id, line_total, move_id, company_currency, current_currency, context=None):
        '''
        Create one account move line, on the given account move, per voucher line where amount is not 0.0.
        It returns Tuple with tot_line what is total of difference between debit and credit and
        a list of lists with ids to be reconciled with this format (total_deb_cred,list_of_lists).

        :param voucher_id: Voucher id what we are working with
        :param line_total: Amount of the first line, which correspond to the amount we should totally split among all voucher lines.
        :param move_id: Account move wher those lines will be joined.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: Tuple build as (remaining amount not allocated on voucher lines, list of account_move_line created in this method)
        :rtype: tuple(float, list of int)
        '''
        if context is None:
            context = {}

        move_line_obj = self.pool.get('account.move.line')
        currency_obj = self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')

        tot_line = line_total
        rec_lst_ids = []

        voucher_brw = self.pool.get('account.voucher').browse(cr, uid, voucher_id, context)
        ctx = context.copy()
        ctx.update({'date': voucher_brw.date})
        for line in voucher_brw.line_ids:
            ctx_line = context.copy()
            #create one move line per voucher line where amount is not 0.0
            if not line.amount:
                continue
    
            amount = line.amount
   
            # convert the amount set on the voucher line into the currency of the voucher's company
            amount = self._convert_amount(cr, uid, amount, voucher_brw.id, context=ctx)

            #amount = currency_obj(cr, uid, voucher_brw.currency_id.id, voucher_brw.company_id.currency_id.id, context=ctx_line)
            amount_real = self._convert_amount(cr, uid, line.amount, voucher_brw.id, context=ctx)
            # if the amount encoded in voucher is equal to the amount unreconciled, we need to compute the
            # currency rate difference
            #if line.amount == line.amount_unreconciled:
                #currency_rate_difference = 0.0 #line.move_line_id.amount_residual - (line.amount * voucher_brw.payment_rate)
            #else:
                #TODO:
                #currency_rate_difference = 0.0 #amount - (line.amount * voucher_brw.payment_rate)

            if line.move_line_id:
                ctx_line.update({'date' : line.move_line_id.date})
                #raise osv.except_osv('a', str(ctx_line))
                #raise osv.except_osv('a', '%s %s' % (str(voucher_brw.currency_id.id), str(voucher_brw.company_id.currency_id.id))) 
                #a = currency_obj._get_conversion_rate(cr, uid, voucher_brw.journal_id.currency, voucher_brw.company_id.currency_id, context=ctx_line)
                #raise osv.except_osv('a', '%s' % (str(a)))
                amount = currency_obj.compute(cr, uid, voucher_brw.journal_id.currency.id, voucher_brw.company_id.currency_id.id, line.amount, context=ctx_line, round=True)
                amount_line = currency_obj.compute(cr, uid, voucher_brw.currency_id.id, voucher_brw.company_id.currency_id.id, line.amount, context=ctx, round=True)
                currency_rate_difference = amount - amount_line
                #raise osv.except_osv('a', '%s' % (str(currency_rate_difference)))
                #amount_move_line = self._convert_amount(cr, uid, line.amount, voucher_brw.id, 
                #currency_rate = amount - 
                #currency_rate_difference = 0.0
            else:
                currency_rate_difference = 0.0

            


            move_line = {
                        'journal_id': voucher_brw.journal_id.id,
                        'period_id': voucher_brw.period_id.id,
                        'name': line.name or '/',
                        'account_id': line.account_id.id,
                        'move_id': move_id,
                        'partner_id': line.partner_id and line.partner_id.id or False,
                        'currency_id' : voucher_brw.journal_id.currency and voucher_brw.journal_id.currency.id or False,
                        # 'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                        # 'analytics_id' : line.analytics_id and line.analytics_id.id or False,
                        'quantity': 1,
                        'credit': 0.0,
                        'debit': 0.0,
                        'date': voucher_brw.date
                        }

            if amount < 0:
                amount = -amount
                if line.type == 'dr':
                    line.type = 'cr'
                else:
                    line.type = 'dr'

            if (line.type=='dr'):
                #tot_line += amount_real
                tot_line += line.amount
                move_line['debit'] = amount
            else:
                #tot_line -= amount_real
                tot_line -= line.amount
                move_line['credit'] = amount

            if voucher_brw.tax_id and voucher_brw.type in ('sale', 'purchase'):
                move_line.update({
                    'account_tax_id': voucher_brw.tax_id.id,
                })

            if move_line.get('account_tax_id', False):
                tax_data = tax_obj.browse(cr, uid, [move_line['account_tax_id']], context=context)[0]
                if not (tax_data.base_code_id and tax_data.tax_code_id):
                    raise osv.except_osv(_('No Account Base Code and Account Tax Code!'),_("You have to configure account base code and account tax code on the '%s' tax!") % (tax_data.name))

            # compute the amount in foreign currency
            foreign_currency_diff = 0.0
            amount_currency = False
            if line.move_line_id:
                voucher_currency = voucher_brw.currency_id and voucher_brw.currency_id.id or voucher_brw.journal_id.company_id.currency_id.id
                # We want to set it on the account move line as soon as the original line had a foreign currency
                if line.move_line_id.currency_id and line.move_line_id.currency_id.id != company_currency:
                    # we compute the amount in that foreign currency. 
                    if line.move_line_id.currency_id.id == current_currency:
                        # if the voucher and the voucher line share the same currency, there is no computation to do
                        sign = (move_line['debit'] - move_line['credit']) < 0 and -1 or 1
                        amount_currency = sign * (line.amount)
                    elif line.move_line_id.currency_id.id == voucher_brw.payment_rate_currency_id.id:
                        # if the rate is specified on the voucher, we must use it
                        voucher_rate = currency_obj.browse(cr, uid, voucher_currency, context=ctx).rate
                        amount_currency = (move_line['debit'] - move_line['credit']) * voucher_brw.payment_rate * voucher_rate
                    else:
                        # otherwise we use the rates of the system (giving the voucher date in the context)
                        #raise osv.except_osv('c','c')
                        amount_currency = currency_obj.compute(cr, uid, company_currency, line.move_line_id.currency_id.id, move_line['debit']-move_line['credit'], context=ctx)
                if line.amount == line.amount_unreconciled and line.move_line_id.currency_id.id == voucher_currency:
                    sign = voucher_brw.type in ('payment', 'purchase') and -1 or 1
                    foreign_currency_diff = sign * line.move_line_id.amount_residual_currency + amount_currency

            move_line['amount_currency'] = amount_currency
            voucher_line = move_line_obj.create(cr, uid, move_line)
            rec_ids = [voucher_line, line.move_line_id.id]

            #raise osv.except_osv('a', '%s' % (str(currency_rate_difference)))
            #raise osv.except_osv('a', '%s' % (str(currency_obj.is_zero(cr, uid, voucher_brw.company_id.currency_id, currency_rate_difference))))


            if not currency_obj.is_zero(cr, uid, voucher_brw.company_id.currency_id, currency_rate_difference):
                #raise osv.except_osv('a', 'b')
                # Change difference entry in company currency
                exch_lines = self._get_exchange_lines(cr, uid, line, move_id, currency_rate_difference, company_currency, current_currency, context=context)
                #tot_line += (exch_lines['debit'] - exch_lines['credit'])
                move_line_obj.create(cr, uid, exch_lines, context)


            if line.move_line_id and line.move_line_id.currency_id and not currency_obj.is_zero(cr, uid, line.move_line_id.currency_id, foreign_currency_diff):
                # Change difference entry in voucher currency
                move_line_foreign_currency =    {
                                                'journal_id': line.voucher_id.journal_id.id,
                                                'period_id': line.voucher_id.period_id.id,
                                                'name': _('change')+': '+(line.name or '/'),
                                                'account_id': line.account_id.id,
                                                'move_id': move_id,
                                                'partner_id': line.partner_id and line.partner_id.id or False,
                                                'currency_id': line.move_line_id.currency_id.id,
                                                'amount_currency': -1 * foreign_currency_diff,
                                                'quantity': 1,
                                                'credit': 0.0,
                                                'debit': 0.0,
                                                'date': line.voucher_id.date,
                                                }
                new_id = move_line_obj.create(cr, uid, move_line_foreign_currency, context=context)
                rec_ids.append(new_id)

            if line.move_line_id.id:
                rec_lst_ids.append(rec_ids)

        return (tot_line, rec_lst_ids)
        
    def writeoff_move_line_get(self, cr, uid, voucher_id, line_total, move_id, name, company_currency, current_currency, partner_id=False, context=None):
        '''
        Set a dict to be use to create the writeoff move line.

        :param voucher_id: Id of voucher what we are creating account_move.
        :param line_total: Amount remaining to be allocated on lines.
        :param move_id: Id of account move where this line will be added.
        :param name: Description of account move line.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: mapping between fieldname and value of account move line to create
        :rtype: dict
        '''
        currency_obj = self.pool.get('res.currency')
        move_line = {}

        voucher_brw = self.pool.get('account.voucher').browse(cr,uid,voucher_id,context)
        current_currency_obj = voucher_brw.currency_id or voucher_brw.journal_id.company_id.currency_id


        if not currency_obj.is_zero(cr, uid, current_currency_obj, line_total):
            diff = line_total
            account_id = False
            write_off_name = ''
            if voucher_brw.payment_option == 'with_writeoff':
                account_id = voucher_brw.writeoff_acc_id.id
                write_off_name = voucher_brw.comment
            elif voucher_brw.type in ('sale', 'receipt'):
                account_id = voucher_brw.partner_id.property_account_receivable.id
            else:
                account_id = voucher_brw.partner_id.property_account_payable.id

            move_line = {
                        'name': write_off_name or name,
                        'account_id': account_id,
                        'move_id': move_id,
                        'partner_id': partner_id,
                        'date': voucher_brw.date,
                        'credit': diff > 0 and diff or 0.0,
                        'debit': diff < 0 and -diff or 0.0,
                        'amount_currency': company_currency <> current_currency and voucher_brw.writeoff_amount or False,
                        'currency_id': company_currency <> current_currency and current_currency or False,
                        # 'analytic_account_id': voucher_brw.analytic_id and voucher_brw.analytic_id.id or False,
                        }

        return move_line

    def _get_exchange_lines(self, cr, uid, line, move_id, amount_residual, company_currency, current_currency, context=None):
        '''
        Prepare the two lines in company currency due to currency rate difference.

        :param line: browse record of the voucher.line for which we want to create currency rate difference accounting
            entries
        :param move_id: Account move wher the move lines will be.
        :param amount_residual: Amount to be posted.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: the account move line and its counterpart to create, depicted as mapping between fieldname and value
        :rtype: tuple of dict
        '''
        if amount_residual > 0:
            account_id = line.voucher_id.company_id.expense_currency_exchange_account_id
            if not account_id:
                raise osv.except_osv(_('Insufficient Configuration!'),_("You should configure the 'Loss Exchange Rate Account' in the accounting settings, to manage automatically the booking of accounting entries related to differences between exchange rates."))
        else:
            account_id = line.voucher_id.company_id.income_currency_exchange_account_id
            if not account_id:
                raise osv.except_osv(_('Insufficient Configuration!'),_("You should configure the 'Gain Exchange Rate Account' in the accounting settings, to manage automatically the booking of accounting entries related to differences between exchange rates."))
        # Even if the amount_currency is never filled, we need to pass the foreign currency because otherwise
        # the receivable/payable account may have a secondary currency, which render this field mandatory
        if line.account_id.currency_id:
            account_currency_id = line.account_id.currency_id.id
        else:
            account_currency_id = company_currency <> current_currency and current_currency or False

        account_currency_id = line.voucher_id.journal_id.currency and line.voucher_id.journal_id.currency.id or line.voucher_id.journal_id.company_id.currency_id.id

        if line.type == 'cr':
            debit = amount_residual > 0 and amount_residual or 0.0
            credit = amount_residual < 0 and -amount_residual or 0.0
        else:
            debit = amount_residual < 0 and -amount_residual or 0.0
            credit = amount_residual > 0 and amount_residual or 0.0

        move_line_counterpart = {
                                'journal_id': line.voucher_id.journal_id.id,
                                'period_id': line.voucher_id.period_id.id,
                                'name': _('Currency Rate Adjustment')+': '+(line.name or '/'),
                                'account_id': account_id.id,
                                'move_id': move_id,
                                'amount_currency': 0.0,
                                'partner_id': line.voucher_id.partner_id.id,
                                'currency_id': account_currency_id,
                                'quantity': 1,
                                'debit': debit,
                                'credit': credit,
                                'date': line.voucher_id.date,
                                }
        return move_line_counterpart
        
        
        
        
        
                            
account_voucher()                           
    
