from openerp.osv import osv,fields
class res_partner(osv.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    _columns = {
            'is_instructor': fields.boolean('Instructor'),
            'session_ids' : fields.one2many('openacademy.session','instructor_id',string='Sessions'),
            }