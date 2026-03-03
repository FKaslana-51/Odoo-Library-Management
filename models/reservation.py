from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryReservation(models.Model):
    _name = 'library.reservation'
    _description = 'Library Book Reservation'
    _order = 'reservation_date asc'

    member_id = fields.Many2one(
        'library.member',
        required=True
    )

    book_id = fields.Many2one(
        'library.book',
        required=True
    )

    reservation_date = fields.Date(
        default=fields.Date.today
    )

    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('notified', 'Notified'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled')
    ], default='waiting')

    @api.constrains('member_id', 'book_id', 'state')
    def _check_duplicate_active_reservation(self):
        for record in self:
            existing = self.search([
                ('member_id', '=', record.member_id.id),
                ('book_id', '=', record.book_id.id),
                ('state', 'in', ['waiting', 'notified']),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(
                    "Member already has an active reservation for this book."
                )