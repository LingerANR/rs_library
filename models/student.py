# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Student(models.Model):
    _inherit = 'res.partner'

    student_value = fields.Boolean(string="Student?")
    # mat = fields.Char(string='Matricula de estudiante', index=True)

    @api.model
    def create(self, vals):
        rec = super(Student,self).create(vals)
        import pdb; pdb.set_trace()
        if rec.student_value == True:
            rec.write({'ref' : self.get_matricula() })
            return rec

        else:
            print("Esta inactivo...")
            return rec

    # @api.model
    # def write(self, vals):
    #     import pdb; pdb.set_trace()
    #     rec = super(Student,self).write(vals)
    #     return rec
    #
    # @api.onchange('student_value')
    # def onchange_parent_id(self):
    #     import pdb; pdb.set_trace()
    #     if self.student_value==True:
    #         if not self.ref:
    #             matricula=self.env['ir.sequence'].next_by_code('res.partner')
    #             m=matricula[:4]+self.name[0]+matricula[4:]
    #             self.ref=matricula
    #             #self.write({'ref' : m })

    def get_matricula(self):
        matricula=self.env['ir.sequence'].next_by_code('res.partner')
        m=matricula[:4]+self.name[0]+matricula[4:]
        return m

    @api.model
    def write(self, vals):
        import pdb; pdb.set_trace()
        if vals.get('student_value',True):
            if vals['student_value']== True:
                if not self.ref:
                    vals['ref']=self.get_matricula()
        rec = super(Student,self).write(vals)

        return rec

    #esto no se debe hacer: bucle infinito
    # @api.model
    # def write(self, vals):
    #     import pdb; pdb.set_trace()
    #     rec = super(Student,self).write(vals)
    #     self.write({'student_value' : False})
    #     return rec
