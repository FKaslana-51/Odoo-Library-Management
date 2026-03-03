from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class LibraryBorrowing(models.Model):
    _name = 'library.borrowing'
    _description = 'Library Borrowing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'borrow_date desc'

    name = fields.Char(
        string='Borrow Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )

    member_id = fields.Many2one(
        'library.member',
        string='Member',
        required=True,
        tracking=True
    )

    borrow_date = fields.Date(
        string='Borrow Date',
        default=fields.Date.today,
        required=True
    )

    due_date = fields.Date(
        string='Due Date',
        required=True
    )

    return_date = fields.Date(
        string='Return Date'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('returned', 'Returned'),
        ('late', 'Late')
    ], default='draft', tracking=True)

    line_ids = fields.One2many(
        'library.borrowing.line',
        'borrowing_id',
        string='Borrowed Books'
    )

    total_books = fields.Integer(
        string='Total Books',
        compute='_compute_total_books'
    )

    fine_amount = fields.Float(
        string='Fine Amount',
        compute='_compute_fine',
        store=True
    )

    active = fields.Boolean(default=True)

    # ======================================
    # CREATE OVERRIDE (SEQUENCE)
    # ======================================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'library.borrowing.sequence'
                ) or 'New'
        return super().create(vals_list)

    # ======================================
    # COMPUTE METHODS
    # ======================================

    def _compute_total_books(self):
        for record in self:
            record.total_books = sum(record.line_ids.mapped('quantity'))

    @api.depends('due_date', 'return_date', 'state')
    def _compute_fine(self):
        for record in self:
            fine = 0
            if record.return_date and record.return_date > record.due_date:
                late_days = (record.return_date - record.due_date).days
                fine = late_days * 5000  # Rp 5000 per day
            record.fine_amount = fine

    # ======================================
    # ACTION METHODS
    # ======================================

    def action_confirm(self):
        for record in self:

            if record.member_id.status != 'active':
                raise ValidationError("Member is blocked.")

            if not record.line_ids:
                raise ValidationError("Add at least one book.")

            for line in record.line_ids:
                if line.book_id.stock_available < line.quantity:
                    raise ValidationError(
                        f"Not enough stock for book: {line.book_id.name}"
                    )

            record.state = 'confirmed'

    def action_return(self):
        for record in self:
            record.return_date = date.today()

            if record.return_date > record.due_date:
                record.state = 'late'
            else:
                record.state = 'returned'

    def action_set_draft(self):
        self.state = 'draft'

    # ======================================
    # CRON METHOD
    # ======================================

    @api.model
    def _cron_check_late(self):
        today = fields.Date.today()

        borrowings = self.search([
            ('state', '=', 'confirmed'),
            ('due_date', '<', today)
        ])

        for record in borrowings:
            record.state = 'late'