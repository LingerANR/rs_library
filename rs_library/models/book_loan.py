# -*- coding: utf-8 -*-
from datetime import timedelta
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
    date_start = fields.Date(string="Loan Start Date", default=fields.Date.today)
    date_end = fields.Date(string="Loan End Date",track_visibility='onchange', compute='_compute_date_end', store=True, inverse='_inverse_date_end', required=True)
    days = fields.Integer(string="Days",compute='_compute_days',store=True, required=True)
    loan_count = fields.Char(string="Numero de prestmo",track_visibility='onchange')

    student_value = fields.Boolean(string="Is Student", related='student_id.student_value',readonly=True,help="Partner is student?")

    @api.depends('days')
    def _inverse_date_end(self):
        for order in self:
            if order.days:
                order.date_end=order.date_start+timedelta(days=order.days)

    def _compute_days(self):
        for order in self:
            if order.date_start and order.date_end:
                order.days=(order.date_end-order.date_start).days
            else:
                order.days=5

    def _compute_date_end(self):
        for order in self:
            if order.date_start and order.days:
                order.date_end=order.date_start+timedelta(days=order.days)
            else:
                if order.date_start:
                    order.date_end=order.date_start+timedelta(days=5)

    @api.model
    def create(self, vals):
        c_loan=self.env['ir.sequence'].next_by_code('book.loan')
        vals['loan_count']=c_loan
        loa = super(BookLoan,self).create(vals)
        return loa

    def action_approve(self):
        self.state="approve"
        for loan in self.loan_line:
            loan.action_approve()

        return True

    def check_loans_status(self):
        approve=False
        over=False
        done=False
        if self.state=='approve' or self.state=='over':
            done_count= 0
            sum_done=len(self.loan_line)
            for loan in self.loan_line:
                if loan.state=='over':
                   over=True
                if loan.state=='approve':
                   approve=True
                if loan.state=='done':
                    done_count=done_count+1
            if over:
                self.state='over'
            else:
                if approve:
                    self.state='approve'
                else:
                    self.state='done'
            if done_count==sum_done:
                self.state='done'

    @api.multi
    def update_loan_status(self):
        loans = self.search([('state','=','approve')])
        for loan in loans:
            if loan.date_end:
                if loan.state=='approve' and fields.Date.today()>loan.date_end:
                    loan.loan_line.update_loan_status()


class BookLoanLines(models.Model):
    _name="book.loan.line"
    _description = "Loan Books Detail"
    _rec_name="book_id"

    @api.model
    def _set_default_start_date(self):
        return self.book_loan_id.date_start

    @api.model
    def _set_default_end_date(self):
        return self.book_loan_id.date_end

    book_loan_id = fields.Many2one('book.loan', string='Loan Reference', required=True, ondelete='cascade', index=True, copy=False)
    book_id = fields.Many2one('book')
    date_start = fields.Date(default=_set_default_start_date)
    date_end = fields.Date(default=_set_default_end_date)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approved'),
        ('denied', 'Denied'),
        ('over', 'Over Dated'),
        ('done', 'Recovered'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')
    student_id=fields.Char(string="Student", related='book_loan_id.student_id.name',readonly=True,help="Student Name")



    def _check_approve(self):
        if self.book_id.quantity>0:
            return True
        else:
            return False

    def action_approve(self):
        if self._check_approve():
            self.state='approve'
            actual_qty=self.book_id.quantity
            self.book_id.quantity=actual_qty-1
        else:
            self.state='denied'

    def action_done(self):
        actual_qty=self.book_id.quantity
        self.book_id.quantity=actual_qty+1
        self.state="done"
        self.book_loan_id.check_loans_status()

    def action_cancel(self):
        actual_state=self.state
        actual_qty=self.book_id.quantity
        if actual_state =='approve' or actual_state =='over':
            self.book_id.quantity=actual_qty+1
            self.state="cancel"
        self.book_loan_id.check_loans_status()

    @api.multi
    def update_loan_status(self):
        for loan in self:
            if loan.date_end:
                if loan.state=='approve' and fields.Date.today()>loan.date_end:
                    vals={
                    'loan_line_id': loan.id,
                    }
                    #import pdb; pdb.set_trace()
                    loan.env['penalty.fee'].create(vals)
                    loan.state='over'

    @api.onchange('book_id')
    def onchange_book_id(self):
        self.date_start=self.book_loan_id.date_start
        self.date_end=self.book_loan_id.date_end


    def action_recovered(self):
        self.action_done()
