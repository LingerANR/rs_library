# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RSGroups(models.Model):
    _name="rs.group"
    _description="School Groups"
    #_inherit = 'res.partner'
    name = fields.Char("Group")


class Student(models.Model):
    _inherit = 'res.partner'

    student_value = fields.Boolean(string="Is Student")
    # mat = fields.Char(string='Matricula de estudiante', index=True)
    rs_group_id = fields.Many2one('rs.group', string="Group")

    @api.model
    def create(self, vals):
        rec = super(Student,self).create(vals)
        import pdb; pdb.set_trace()
        if rec.student_value == True:
            rec.write({'ref' : rec.get_matricula() })
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

    @api.multi
    def write(self, vals):
        rec = super(Student,self).write(vals)
        if vals.get('student_value',False):
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
