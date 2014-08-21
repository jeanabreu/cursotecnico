from openerp.osv import osv,fields
class openacademy_enroll(osv.Model):
    _name = "openacademy.enroll"
    _columns = {
            'session_id': fields.many2one('openacademy.session',string='Session'),
            'atendee_ids': fields.one2many('openacademy.enroll.atendee','enroll_id',string='Atendee'),            
        } 
        
class openacademy_enroll_atendee(osv.Model):
    _name = "openacademy.enroll.atendee"
    _columns = {
            'name': fields.char('Name',32, required=True),
            'partner_id': fields.many2one('res.partner', string='Partner'),
            'enroll_id' : fields.many2one('openacademy.enroll',string='Enroll')

        } 
