from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBorrowingLine(models.Model):
    _name = 'library.borrowing.line'
    _description = 'Library Borrowing Line'
    _order = 'id desc'

    borrowing_id = fields.Many2one(
        'library.borrowing',
        string='Borrowing',
        required=True,
        ondelete='cascade'
    )

    book_id = fields.Many2one(
        'library.book',
        string='Book',
        required=True,
        ondelete='restrict'
    )

    quantity = fields.Integer(
        string='Quantity',
        required=True,
        default=1
    )

    returned_qty = fields.Integer(
        string='Returned Quantity',
        default=0
    )

    # =====================================
    # CONSTRAINTS
    # =====================================

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

    @api.constrains('returned_qty')
    def _check_returned_qty(self):
        for record in self:
            if record.returned_qty < 0:
                raise ValidationError("Returned quantity cannot be negative.")

            if record.returned_qty > record.quantity:
                raise ValidationError("Returned quantity cannot exceed borrowed quantity.")

    @api.constrains('book_id', 'borrowing_id')
    def _check_duplicate_book(self):
        for record in self:
            duplicate = self.search([
                ('borrowing_id', '=', record.borrowing_id.id),
                ('book_id', '=', record.book_id.id),
                ('id', '!=', record.id)
            ])
            if duplicate:
                raise ValidationError("The same book cannot be added twice in one borrowing transaction.")