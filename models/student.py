# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Student(models.Model):
    _inherit = 'res.partner'

    student_value = fields.Boolean(string="Student?", default=False)
    # mat = fields.Char(string='Matricula de estudiante', index=True)
