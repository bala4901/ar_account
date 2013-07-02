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

	_columns =	{
							'account_writeoff_id' : fields.many2one(string='Default Write-Off Account', obj='account.account', domain=['|',('type','!=','view'),('type','!=','closed'),('type','!=','consolidation')]),
							'account_balance_sheet_id' : fields.many2one(string='Balance Sheet Account', obj='account.account', domain=[('type','=','view')]),
							'account_profit_loss_id' : fields.many2one(string='Profit Loss Account', obj='account.account', domain=[('type','=','view')]),
							'account_asset_id' : fields.many2one(string='Asset Account', obj='account.account', domain=[('type','=','view')]),
							'account_activa_id' : fields.many2one(string='Activa Account', obj='account.account', domain=[('type','=','view')]),
							'account_pasiva_id' : fields.many2one(string='Pasiva Account', obj='account.account', domain=[('type','=','view')]),
							'account_liabillity_id' : fields.many2one(string='Liabillity Account', obj='account.account', domain=[('type','=','view')]),
							'account_equity_id' : fields.many2one(string='Equity Account', obj='account.account'),
							'account_income_id' : fields.many2one(string='Income Account', obj='account.account', domain=[('type','=','view')]),
							'account_cogs_id' : fields.many2one(string='CoGS Account', obj='account.account', domain=[('type','=','view')]),
							'account_expense_id' : fields.many2one(string='Expense Account', obj='account.account', domain=[('type','=','view')]),
							'account_other_income_id' : fields.many2one(string='Other Income Account', obj='account.account', domain=[('type','=','view')]),
							'account_other_expense_id' : fields.many2one(string='Other Expense Account', obj='account.account', domain=[('type','=','view')]),
							'account_root_id' : fields.many2one(string='Root Account', obj='account.account', domain=[('type','=','view')]),
							'account_equity1_id' : fields.many2one(string='Equity Account', obj='account.account', domain=[('type','=','view')]),
							'account_pl_id' : fields.many2one(string='Profit Loss Account', obj='account.account'),
							'account_deviden_id' : fields.many2one(string='Deviden Account', obj='account.account'),
							}
res_company()




