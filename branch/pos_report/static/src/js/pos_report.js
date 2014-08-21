openerp.pos_partner = function(instance){
	var QWeb = instance.web.qweb,
    _t = instance.web._t;
	
    instance.pos_partner = {};
    
    var module = instance.pos_partner;
	
	openerp_pos_partner_validate(instance,module); //import validate.js
	
	
	instance.point_of_sale.PaymentScreenWidget = instance.point_of_sale.PaymentScreenWidget.extend({
		start: function(){
            this._super();
            var self = this;
            self.$el.find('.oe_pos_partner-search-vat-number').on('click', self, function(r) {
                self.searchVatNumber(r);
            });
            //var paymentVat = new module.PaymentVatWidget(this);
            //paymentVat.appendTo(this.$el);
            //console.log(this.getChildren()[0].$el);
        },
        searchVatNumber: function(e){
        	var self = this;
        	self.$el.find('.oe_pos_partner-payment-vat-name')[0].style.visibility = 'visible';
       		console.log(e);
        },
        changePaymentVatNumber: function(e){
        	var newVatNumber = event.currentTarget.value;
            var vatNumber = parseFloat(newVatNumber);
            if(!isNaN(vatNumber)){
                this.vatNumber = vatNumber;
                //this.payment_line.set_amount(amount);
            }
        	console.log(e);
        },
        focusInPaymentVatNumber: function(e){
        	//this.set_numpad_vat(this.pos_widget.numpad.state);
        	console.log('focusIn event');
        	console.log(e);
        },
        focusOutPaymentVatNumber: function(e){
        	//this.unset_numpad_vat();
        	console.log('focusOut event');
        	console.log(e);
        },
        renderElement: function() {
            var self = this;
            this._super();
            this.$el.find('.oe_pos_partner-payment-vat-number-value').keyup(function(event){
                self.changePaymentVatNumber(event);
            });
            this.$el.find('.oe_pos_partner-payment-vat-number-value').focusin(function(event){
                self.focusInPaymentVatNumber(event);
            });
            this.$el.find('.oe_pos_partner-payment-vat-number-value').focusout(function(event){
                self.focusOutPaymentVatNumber(event);
            });
        },
        unset_numpad_vat: function() {
        	this.set_numpad_vat(null);
        	this.set_numpad_state(this.pos_widget.numpad.state);
        },
        set_numpad_vat: function(numpadState) {
        	if (this.numpadState) {
        		this.numpadState.unbind('set_value', this.set_valueVat);
        		this.numpadState.unbind('change:mode', this.setNumpadModeVat);
        	}
        	this.numpadState = numpadState;
        	if (this.numpadState) {
        		this.numpadState.bind('set_value', this.set_valueVat, this);
        		this.numpadState.bind('change:mode', this.setNumpadModeVat, this);
        		this.numpadState.reset();
        		this.setNumpadModeVat();
        	}
        },
        setNumpadModeVat: function() {
    		this.numpadState.set({mode: 'paymentVat'});
    	},
        set_valueVat: function(val) {
        	console.log(val);
        },
	});
	
	
	var _superOrder = instance.point_of_sale.Order
	instance.point_of_sale.Order = instance.point_of_sale.Order.extend({
		initialize: function(attributes){
			var _this = _superOrder.prototype.initialize.apply(this, arguments)
			_this.set({
				'vat_number': '',
				'vat_name': '',
				'partner_id': 0,
			});
			return _this;
		},
        getVatNumber: function() {
            return this.get('vat_number');
        },
        getVatName: function() {
            return this.get('vat_name');
        },
        getPartnerId: function() {
            return this.get('partner_id');
        },
        exportAsJSON: function() {
        	var _res = _superOrder.prototype.exportAsJSON.apply(this, arguments);
        	_res['vat_number'] = this.getVatNumber();
        	_res['vat_name'] = this.getVatName();
        	_res['partner_id'] = this.getPartnerId();
        	return _res 
        },
	});
};