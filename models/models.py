# from odoo import models, fields, api


# class library_fin(models.Model):
#     _name = 'library_fin.library_fin'
#     _description = 'library_fin.library_fin'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

