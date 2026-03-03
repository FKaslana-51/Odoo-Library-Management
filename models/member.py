from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'member_code asc'

    name = fields.Char(
        string='Member Name',
        required=True,
        tracking=True
    )

    member_code = fields.Char(
        string='Member ID',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )

    email = fields.Char(
        string='Email'
    )

    phone = fields.Char(
        string='Phone'
    )

    status = fields.Selection([
        ('active', 'Active'),
        ('blocked', 'Blocked')
    ], default='active', tracking=True)

    borrow_ids = fields.One2many(
        'library.borrowing',
        'member_id',
        string='Borrowings'
    )

    total_borrowed = fields.Integer(
        string='Total Borrowed',
        compute='_compute_statistics'
    )

    total_late = fields.Integer(
        string='Total Late',
        compute='_compute_statistics'
    )

    active = fields.Boolean(
        default=True
    )

    # ======================================
    # CREATE OVERRIDE (SEQUENCE)
    # ======================================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('member_code', 'New') == 'New':
                vals['member_code'] = self.env['ir.sequence'].next_by_code(
                    'library.member.sequence'
                ) or 'New'
        return super().create(vals_list)

    # ======================================
    # COMPUTE METHODS
    # ======================================

    def _compute_statistics(self):
        for record in self:
            record.total_borrowed = len(record.borrow_ids)
            record.total_late = len(record.borrow_ids.filtered(lambda b: b.state == 'late'))

    # ======================================
    # CONSTRAINT
    # ======================================

    @api.constrains('email')
    def _check_unique_email(self):
        for record in self:
            if record.email:
                existing = self.search([
                    ('email', '=', record.email),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError("Email must be unique.")