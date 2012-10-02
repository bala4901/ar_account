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

class ir_sequence_period(osv.osv):
    _name = 'ir.sequence.period'
    _rec_name = "sequence_main_id"
    _columns = {
        "sequence_id": fields.many2one("ir.sequence", 'Sequence', required=True, ondelete='cascade'),
        "sequence_main_id": fields.many2one("ir.sequence", 'Main Sequence', required=True, ondelete='cascade'),
        "period_id": fields.many2one('account.period', 'Period', required=True, ondelete='cascade')
    }

    _sql_constraints = [
        ('main_id', 'CHECK (sequence_main_id != sequence_id)',  'Main Sequence must be different from current !'),
    ]

ir_sequence_period()

class ir_sequence(osv.osv):
    _inherit = 'ir.sequence'
    _columns = {
        'period_ids' : fields.one2many('ir.sequence.period', 'sequence_main_id', 'Sequences')
    }

ir_sequence()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
