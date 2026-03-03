{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Advanced Library Management System',
    'description': """
        Advanced Library Management System for Odoo 19
        Features:
        - Multi book borrowing
        - Fine calculation
        - Auto late detection
        - Smart dashboard ready
    """,
    'author': 'Fircan',
    'category': 'Services',
    'depends': ['base', 'mail'],
    'data': [
    'security/ir.model.access.csv',
    'data/sequence.xml',
    'data/cron.xml',

    # VIEWS FIRST
    'views/book_views.xml',
    'views/member_views.xml',
    'views/borrowing_views.xml',
    'views/reservation_views.xml',
    'views/return_log_views.xml',

   # MENU LAST
    'views/menu.xml',
],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}