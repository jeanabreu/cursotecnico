function openerp_pos_sequence_jquery(instance, module){
	
	jQuery.ajaxSettings['asyncPreventDefault'] = false;
	
	jQuery.Event.prototype.isDefaultPrevented = 
		function(){
			if (!jQuery.ajaxSettings.async && jQuery.ajaxSettings.asyncPreventDefault){
				return true;
			}
			return false;
		}
}