openerp.pos_sequence = function(instance){
	
    instance.pos_sequence = {};
    
    var module = instance.pos_sequence;
	
	openerp_pos_sequence_jquery(instance,module); //import jquery.js
	
	openerp_pos_sequence_widgets(instance,module); //import widgets	.js
	
	var _superPosModel = instance.point_of_sale.PosModel;
	instance.point_of_sale.PosModel = instance.point_of_sale.PosModel.extend({
	    load_server_data: function() {
	    	var self = this;
	    	var _def = _superPosModel.prototype.load_server_data.apply(this, arguments);
	    	_def.then(function(){
	    		return self.fetch(
                        'pos.config',
                        ['individual_accounting'],
                        [['id','=', self.get('pos_session').config_id[0]]]
                    );
	    	}).then(function(configs){
	    		self.get('pos_config')['individual_accounting'] = configs[0]['individual_accounting'];
	    		return self.fetch('account.journal',['id','name','sequence_id','code'],[['id','in',[self.get('pos_config').journal_id[0]]]]);
	    	}).then(function(sale_journals){
	    		var sequence_ids = [];
	    		var _saleJournals = {};
	    		_.each(sale_journals,function(sale_journal){
	    			_saleJournals[sale_journal.id] = sale_journal;
	    			sequence_ids.push(sale_journal.sequence_id[0]);
	    		});
	    		self.set('sale_journals',_saleJournals);
	    		return (new instance.web.Model('ir.sequence')).call('dict_by_ids',[sequence_ids]);
	    	}).then(function(sale_sequences){
	    		var _sale_journals = self.get('sale_journals');
	    		var _pendingOrders = {};
	    		_.each(self.db.get_orders(),function(order){
	    			if(!_pendingOrders[order.data.sale_journal]){
	    				_pendingOrders[order.data.sale_journal] = 1;
	    			}else{
	    				_pendingOrders[order.data.sale_journal] += 1;
	    			}
	    		});
	    		_.each(Object.keys(_sale_journals),function(saleJournal_id){
	    			var sale_sequence_id = _sale_journals[saleJournal_id].sequence_id[0];
	    			var _increment = sale_sequences[sale_sequence_id].number_increment * _pendingOrders[saleJournal_id]?_pendingOrders[saleJournal_id]:0;
	    			_sale_journals[saleJournal_id]['sequence_prefix'] = sale_sequences[sale_sequence_id].prefix;
	    			_sale_journals[saleJournal_id]['sequence_padding'] = sale_sequences[sale_sequence_id].padding;
	    			_sale_journals[saleJournal_id]['sequence_number_next'] = sale_sequences[sale_sequence_id].number_next + _increment;
	    			_sale_journals[saleJournal_id]['sequence_suffix'] = sale_sequences[sale_sequence_id].suffix;
	    			_sale_journals[saleJournal_id]['sequence_number_increment'] = sale_sequences[sale_sequence_id].number_increment;
	    		});
	    		self.set('sale_journals',_sale_journals);
	    	});
	    	return _def;
	    },
	    push_order: function(record) {
	    	if (this.get('pos_config').individual_accounting){
	    		this.generateOrderNumber(record);
	    	};
	    	return _superPosModel.prototype.push_order.apply(this, arguments);
	    },
	    generateOrderNumber: function(record) {
			var self = this;
			if (record['number'] != '/') {
	    		return ;
	    	};
	    	var _async = jQuery.ajaxSettings.async;
	    	var _asyncPreventDefault = jQuery.ajaxSettings.asyncPreventDefault;
	    	var _sale_journals = self.get('sale_journals');
	    	var _number = '';
			
			_number = _sale_journals[record.sale_journal].sequence_prefix;
			_number += _.string.pad(_sale_journals[record.sale_journal].sequence_number_next,
				_sale_journals[record.sale_journal].sequence_padding,'0');
			_number += _sale_journals[record.sale_journal].sequence_suffix; 
			_sale_journals[record.sale_journal]['sequence_number_next'] = _sale_journals[record.sale_journal].sequence_number_next + _sale_journals[record.sale_journal].sequence_number_increment;
			self.set('sale_journals',_sale_journals);
	    	record.number = _number;
	    	console.log('Sequence generated on offline: ' + _number);
	    	if (self.db.get_orders().length > 0){
	    		return;
	    	};
	    	
	    	jQuery.ajaxSettings.async = false;
	    	jQuery.ajaxSettings.asyncPreventDefault = true;
	    	(new instance.web.Model('ir.sequence')).call('dict_next_by_id',[_sale_journals[record.sale_journal].sequence_id[0]])
	    		.then(function(result){
	    			console.log('Sequence fetched: '+result.next);
	    			record.number = result.next;
	    			record.sequence_sync = true;
	    			_sale_journals[record.sale_journal]['sequence_prefix'] = result.prefix;
	    			_sale_journals[record.sale_journal]['sequence_padding'] = result.padding;
	    			_sale_journals[record.sale_journal]['sequence_number_next'] = result.number_next + result.number_increment;
	    			_sale_journals[record.sale_journal]['sequence_suffix'] = result.suffix;
	    			_sale_journals[record.sale_journal]['sequence_number_increment'] = result.number_increment;
	    			self.set('sale_journals',_sale_journals);
	    		})
	    		.fail(function(error, event){
	    			console.error('Error on get the sequence',error);
	    		});
	    	this.get('selectedOrder').attributes.number = record.number;
	    	this.current_pos_widget.receipt_screen.refresh();
	    	jQuery.ajaxSettings.async = _async;
	    	jQuery.ajaxSettings.asyncPreventDefault = _asyncPreventDefault;
        },
	});
	
	var _superOrder = instance.point_of_sale.Order;
	instance.point_of_sale.Order = instance.point_of_sale.Order.extend({
		initialize: function(attributes){
			var _this = _superOrder.prototype.initialize.apply(this, arguments);
			_this.set({
				'number': '/',
				'sequence_sync': false,
				'sale_journal': attributes.pos.get('pos_config').journal_id[0],
			});
			return _this;
		},
        getNumber: function() {
            return this.get('number');
        },
        getSequenceSync: function() {
            return this.get('sequence_sync');
        },
        getSaleJournal: function() {
            return this.get('sale_journal');
        },
        exportAsJSON: function() {
        	var _res = _superOrder.prototype.exportAsJSON.apply(this, arguments);
        	_res['number'] = this.getNumber();
        	_res['sequence_sync'] = this.getSequenceSync();
        	_res['sale_journal'] = this.getSaleJournal();
        	return _res ;
        },
        export_for_printing: function() {
        	var _res = _superOrder.prototype.export_for_printing.apply(this, arguments);
        	_res['number'] = this.getNumber();
        	_res['sale_journal'] = this.getSaleJournal();
        	return _res ;
        },
	});
	
};