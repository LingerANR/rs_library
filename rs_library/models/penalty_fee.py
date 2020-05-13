# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PenaltyFee(models.Model):
    _name = 'penalty.fee'
    _description = "Penalty loans"

    loan_line_id = fields.Many2one('book.loan.line', string='Loan Reference', required=True, ondelete='cascade', index=True, copy=False)
    paid = fields.Boolean(default=False)
    create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which penalty feed is created.")
    student_id = fields.Many2one('res.partner', string="Student:",track_visibility='onchange')
