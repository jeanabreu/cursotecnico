from openerp.osv import osv,fields
class openacademy_course(osv.Model):
    _name = "openacademy.course"
    _columns = {
            'name': fields.char('Name',32)} 
