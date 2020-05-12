# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class Book(models.Model):
    _name = 'book'
    _description = "Books"

    _rec_name="title"

    photo = fields.Binary("Image", attachment=True)

    photo_medium = fields.Binary("Medium-sized image", attachment=True,
        help="Medium-sized image of this contact. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views.")

    photo_small = fields.Binary("Small-sized image", attachment=True,
            help="Small-sized image of this contact. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required.")

    photo = fields.Binary("Image", attachment=True)
    title = fields.Char(string = "Title")
    isbn = fields.Char(string = "ISBN")
    author = fields.Char(string = "Author")
    quantity = fields.Integer(string="Existance")
    description = fields.Text()

    @api.model
    def create(self,vals):
        if vals.get('photo'):
            vals['photo_small']=vals['photo']
            vals['photo_medium']=vals['photo']
            tools.image_resize_images(vals, sizes={'photo': (1024, None),'photo_small': (64, None),'photo_medium': (128, None)})
        books = super(Book, self).create(vals)
        return books

    @api.multi
    def write(self,vals):
        if vals.get('photo'):
            #import pdb; pdb.set_trace()
            vals['photo_small']=vals['photo']
            vals['photo_medium']=vals['photo']
            tools.image_resize_images(vals, sizes={'photo': (1024, None),'photo_small': (64, None),'photo_medium': (128, None)})
        books = super(Book, self).write(vals)
        return books
