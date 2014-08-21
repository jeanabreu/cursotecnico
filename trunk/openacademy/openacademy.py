from openerp.osv import osv,fields
from datetime import datetime,timedelta
class openacademy_course(osv.Model):
    _name = "openacademy.course"
    _columns = {
            'name': fields.char('Name',32,required=True),
            'description' : fields.text('Description'),
            'session_ids' : fields.one2many('openacademy.session','course_id', string='Sessions'),
            'responsible_id': fields.many2one('res.users',string='Responsible'),            
        } 
    _sql_constraints=[('name_unique','unique(name)','name must be unique')]
    
    def copy(self,cr, uid, id, defaults,context=None):
        course=self.browse(cr,uid,id,context=context)
        defaults['name']=course.name+'copy'
        return super(openacademy_course,self).copy(cr, uid, id, defaults,context=context)
    
        
class openacademy_session(osv.Model):
    def _stopdate(self,cr,uid,ids,field,arg,context=None):
        res={}
        for session in self.browse(cr,uid,ids,context=context):
            end = (datetime.strptime(session.startdate,'%Y-%m-%d')+timedelta(days=session.duration))
            res[session.id]=end.strftime('%Y-%m-%d')
        return res
    def _set_stop_date(self,cr, uid, id, field,value,arg,context=None):
        session=self.browse(cr,uid,id,context=context)
        days=datetime.strptime(value,'%Y-%m-%d') - datetime.strptime(session.startdate,'%Y-%m-%d')
        return self.write(cr,uid,[id],{'duration':days.days},context=context)
    _name = "openacademy.session"
    _columns = {
            'name': fields.char('Name',32,required=True),
            'duration' : fields.float('Duration'),
            'seats' : fields.integer('Seats'),
            'startdate' : fields.date('Start Date'),
            'course_id' : fields.many2one('openacademy.course',string='Course'),
            'atendee_ids': fields.one2many('openacademy.atendee','session_id',string='Atendees'),
            'instructor_id': fields.many2one('res.partner', string='Instructor',
                                             domain = ['|',('is_instructor','=',True),('category_id.name','in',['Instructor Nivel I','Instructor Nivel II'])]),
            'active': fields.boolean('Active'),
            'stopdate' : fields.function(_stopdate,string='StopDate',type='date',
                                         fnct_inv=_set_stop_date),
            'state' : fields.selection([('draft','Draft'),
                                        ('confirm','Confirm'),
                                        ('aproved','Aproved'),
                                        ('done','Done')],string='State',readonly=True),
            
        } 
    _defaults ={
            'active' : True,
            'startdate' : fields.date.today, 
            'state' : 'draft',
            }
    def action_draft(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'draft'},context=context)
    def action_confirm(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'confirm'},context=context)
    def action_done(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'done'},context=context)
    def action_aproved(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'aproved'},context=context)
class openacademy_atendee(osv.Model):
    _name = "openacademy.atendee"
    _columns = {
            'name': fields.char('Name',32, required=True),
            'session_id': fields.many2one('openacademy.session',string='Session'),
            'partner_id': fields.many2one('res.partner', string='Partner'),

        } 
