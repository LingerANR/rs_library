# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PenaltyFee(models.Model):
    _name = 'penalty.fee'
    _description = "Penalty loans"
    _rec_name="student_id"

    loan_line_id = fields.Many2one('book.loan.line', string='Loan Reference', required=True, ondelete='cascade', index=True, copy=False)
    paid = fields.Boolean(default=False)
    create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which penalty feed is created.")
#    student_id = fields.Many2one('res.partner', string="Student:",track_visibility='onchange')
    student_id=fields.Char(string="Student", related='loan_line_id.student_id',readonly=True,help="Student Name")


    def action_paid(self):
        self.paid=True
        self.loan_line_id.action_recovered()
