from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    name = fields.Char(
        string='Book Title',
        required=True,
        tracking=True
    )

    author = fields.Char(
        string='Author',
        required=True
    )

    isbn = fields.Char(
        string='ISBN',
        tracking=True
    )

    category_id = fields.Many2one(
        'library.book.category',
        string='Category',
        ondelete='restrict'
    )

    stock_total = fields.Integer(
        string='Total Stock',
        required=True,
        default=1,
        tracking=True
    )

    stock_available = fields.Integer(
        string='Available Stock',
        compute='_compute_stock_available',
        store=True
    )

    active = fields.Boolean(
        default=True
    )

    borrowing_line_ids = fields.One2many(
        'library.borrowing.line',
        'book_id',
        string='Borrowing Lines'
    )

    # =====================================
    # COMPUTE METHODS
    # =====================================

    @api.depends('stock_total', 'borrowing_line_ids.returned_qty', 'borrowing_line_ids.quantity')
    def _compute_stock_available(self):
        for record in self:
            borrowed_qty = 0
            for line in record.borrowing_line_ids:
                borrowed_qty += (line.quantity - line.returned_qty)

            record.stock_available = record.stock_total - borrowed_qty

    # =====================================
    # CONSTRAINTS
    # =====================================

    @api.constrains('stock_total')
    def _check_stock_total(self):
        for record in self:
            if record.stock_total < 0:
                raise ValidationError("Total stock cannot be negative.")

    @api.constrains('isbn')
    def _check_unique_isbn(self):
        for record in self:
            if record.isbn:
                existing = self.search([
                    ('isbn', '=', record.isbn),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError("ISBN must be unique.")