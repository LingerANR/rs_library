# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Book(models.Model):
    _name = 'book'
    _description = "Books"

    _rec_name="title"

    photo = fields.Binary("Image", attachment=True)
    title = fields.Char(string = "Title")
    isbn = fields.Char(string = "ISBN")
    author = fields.Char(string = "Author")
    quantity = fields.Integer(string="Existance")
    description = fields.Text()
