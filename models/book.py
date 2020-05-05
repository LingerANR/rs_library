# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Book(models.Model):
    _name = 'book'
    _rec_name="title"

    title = fields.Char(string = "Title")
    isbn = fields.Char(string = "ISBN")
    author = fields.Char(string = "Author")
    quantity = fields.Integer(string="Existance")
    description = fields.Text()

class BookLoan(models.Model):
    _name = 'book.loan'

    student_id = fields.Many2one('res.partner')
    loan_line = fields.One2many('book.loan.line', 'book_loan_id', string='Loan Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approved'),
        ('denied', 'Denied'),
        ('over', 'Over Dated'),
        ('done', 'Recovered'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')

    date_record = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    renews = fields.Integer(string="Renews",default=0, help="Number of actual renews")
    date_start = fields.Date()
    date_end = fields.Date()
    days = fields.Integer(string="Days")



class BookLoanLines(models.Model):
    _name="book.loan.line"

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
