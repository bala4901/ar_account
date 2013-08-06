# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright Camptocamp SA 2011
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


from report import report_sxw
from tools.translate import _
import pooler
from datetime import datetime

class BalanceSheetWebKit(report_sxw.rml_parse):

    def __init__(self, cursor, uid, name, context):
        super(BalanceSheetWebKit, self).__init__(cursor, uid, name, context=context)

        self.localcontext.update({
			'time' : time,
        })

HeaderFooterTextWebKitParser('report.report_balance_sheet_webkit',
                             'account.account',
                             'addons/ar_account/report/templates/account_report_balance_sheet.mako',
                             parser=BalanceSheetWebKit)
