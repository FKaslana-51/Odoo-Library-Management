from odoo import models, fields


class LibraryReturnLog(models.Model):
    _name = 'library.return.log'
    _description = 'Library Return History'
    _order = 'return_date desc'

    borrowing_id = fields.Many2one(
        'library.borrowing',
        required=True,
        ondelete='cascade'
    )

    member_id = fields.Many2one(
        'library.member',
        required=True
    )

    book_id = fields.Many2one(
        'library.book',
        required=True
    )

    return_date = fields.Date(
        required=True
    )

    late_days = fields.Integer()

    fine_amount = fields.Float()