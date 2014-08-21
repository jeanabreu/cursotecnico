function openerp_pos_sequence_widgets(instance, module){

	instance.point_of_sale.PosWidget = instance.point_of_sale.PosWidget.extend({
		start: function(){
            this._super();
            this.pos['current_pos_widget'] = this;
        },
    });

}