# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BookLoan(models.Model):
    _name = 'book.loan'
    _description = "Loan Books"
    _rec_name="loan_count"
    _inherit = ['portal.mixin','mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('res.partner', string="Student:",track_visibility='onchange')
    loan_line = fields.One2many('book.loan.line', 'book_loan_id', string='Loan Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approved'),
        ('denied', 'Denied'),
        ('over', 'Over Dated'),
        ('done', 'Recovered'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=False, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')

    date_record = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    renews = fields.Integer(string="Renews",default=0, help="Number of actual renews")
    date_start = fields.Date(string="Loan Start Date")
    date_end = fields.Date(string="Loan End Date",track_visibility='onchange')
    days = fields.Integer(string="Days")
    loan_count = fields.Char(string="Numero de prestmo",track_visibility='onchange')


    @api.model
    def create(self, vals):
        c_loan=self.env['ir.sequence'].next_by_code('book.loan')
        vals['loan_count']=c_loan
        loa = super(BookLoan,self).create(vals)
        return loa

    def action_approve(self):
        self.state="approve"
        for loan in self.loan_line:
            loan.state="approve"

        return True


class BookLoanLines(models.Model):
    _name="book.loan.line"
    _description = "Loan Books Detail"
    _rec_name="book_id"

    book_loan_id = fields.Many2one('book.loan', string='Loan Reference', required=True, ondelete='cascade', index=True, copy=False)
    book_id = fields.Many2one('book')
    date_start = fields.Date()
    date_end = fields.Date()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approved'),
        ('denied', 'Denied'),
        ('over', 'Over Dated'),
        ('done', 'Recovered'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')
