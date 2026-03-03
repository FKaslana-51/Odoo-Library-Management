from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _order = 'name asc'

    name = fields.Char(
        string='Category Name',
        required=True
    )

    description = fields.Text(
        string='Description'
    )

    active = fields.Boolean(
        default=True
    )

    book_ids = fields.One2many(
        'library.book',
        'category_id',
        string='Books'
    )

    book_count = fields.Integer(
        string='Total Books',
        compute='_compute_book_count'
    )

    # =============================
    # COMPUTE METHODS
    # =============================

    @api.depends('book_ids')
    def _compute_book_count(self):
        for record in self:
            record.book_count = len(record.book_ids)

    # =============================
    # CONSTRAINT
    # =============================

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError("Category name must be unique.")