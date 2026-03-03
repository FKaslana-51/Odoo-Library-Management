from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

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

    from datetime import date

    expiry_date = fields.Date(
        string='Membership Expiry Date',
        tracking=True
    )

    is_expired = fields.Boolean(
        string='Expired',
        compute='_compute_is_expired',
        store=True
    )
    membership_duration = fields.Integer(
        string="Membership Duration (Months)",
        default=1
    )

    expiry_date = fields.Date(
        string="Expiry Date",
        compute="_compute_expiry_date",
        store=True
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
    # EXPIRY CHECK
    # ======================================
    @api.depends('expiry_date')
    def _compute_is_expired(self):
        today = fields.Date.today()
        for record in self:
            record.is_expired = bool(
                record.expiry_date and record.expiry_date < today
            )
    
    # ======================================
    # EXPIRY CHECK
    # ======================================
    @api.model
    def _cron_check_membership_expiry(self):
        today = date.today()
        expired_members = self.search([
            ('expiry_date', '<', today),
            ('status', '=', 'active')
        ])
        expired_members.write({'status': 'blocked'})

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
   
    # ======================================
    # MEMBERSHIP DURATION & EXPIRY
    # ====================================== 
    @api.depends('create_date', 'membership_duration')
    def _compute_expiry_date(self):
        for record in self:
            if record.create_date:
                record.expiry_date = (
                    record.create_date.date()
                    + relativedelta(months=record.membership_duration)
                )
            else:
                record.expiry_date = False