# -*- coding: utf-8 -*-
{
    'name': "Book Loan System",

    'summary': """
        Loan Books System""",

    'description': """
        Loan Books System
    """,

    'author': "Real Systems- Edgar Giovanni",
    'website': "https://www.realsystems.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customization',
    'version': '12.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal'],

    # always loaded
    'data': [
        'security/rs_library_security.xml',
        'security/ir.model.access.csv',
        'views/book_loan_views.xml',
        'views/book_views.xml',
        'views/res_partner_view.xml',
        'views/rs_library_views.xml',
        'views/templates.xml',
        'data/ir_sequence_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
