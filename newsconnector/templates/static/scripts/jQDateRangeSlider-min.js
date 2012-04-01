/*
 jQRangeSlider
 A javascript slider selector that supports dates

 Copyright (C) Guillaume Gautreau 2012
 Dual licensed under the MIT or GPL Version 2 licenses.

*/
(function(c){c.widget("ui.dateRangeSlider",c.ui.rangeSlider,{options:{bounds:{min:new Date(2010,0,1),max:new Date(2012,0,1)},defaultValues:{min:new Date(2010,1,11),max:new Date(2011,1,11)}},_create:function(){c.ui.rangeSlider.prototype._create.apply(this);this.element.addClass("ui-dateRangeSlider")},destroy:function(){this.element.removeClass("ui-dateRangeSlider");c.ui.rangeSlider.prototype.destroy.apply(this)},_setOption:function(a,b){(a==="defaultValues"||a==="bounds")&&typeof b!=="undefined"&&
b!==null&&typeof b.min!=="undefined"&&typeof b.max!=="undefined"&&b.min instanceof Date&&b.max instanceof Date?c.ui.rangeSlider.prototype._setOption.apply(this,[a,{min:b.min.valueOf(),max:b.max.valueOf()}]):c.ui.rangeSlider.prototype._setOption.apply(this,this._toArray(arguments))},option:function(a){if(a==="bounds"||a==="defaultValues"){var b=c.ui.rangeSlider.prototype.option.apply(this,arguments);return{min:new Date(b.min),max:new Date(b.max)}}return c.ui.rangeSlider.prototype.option.apply(this,
this._toArray(arguments))},_defaultFormat:function(a){var b=a.getMonth()+1,c=a.getDate();return""+a.getFullYear()+"-"+(b<10?"0"+b:b)+"-"+(c<10?"0"+c:c)},_format:function(a){return c.ui.rangeSlider.prototype._format.apply(this,[new Date(a)])},values:function(a,b){var d=null,d=typeof a!=="undefined"&&typeof b!=="undefined"&&a instanceof Date&&b instanceof Date?c.ui.rangeSlider.prototype.values.apply(this,[a.valueOf(),b.valueOf()]):c.ui.rangeSlider.prototype.values.apply(this,this._toArray(arguments));
return{min:new Date(d.min),max:new Date(d.max)}},min:function(a){if(typeof a!=="undefined"&&a instanceof Date)return new Date(c.ui.rangeSlider.prototype.min.apply(this,[a.valueOf()]));return new Date(c.ui.rangeSlider.prototype.min.apply(this))},max:function(a){if(typeof a!=="undefined"&&a instanceof Date)return new Date(c.ui.rangeSlider.prototype.max.apply(this,[a.valueOf()]));return new Date(c.ui.rangeSlider.prototype.max.apply(this))},bounds:function(a,b){var d;d=typeof a!=="undefined"&&a instanceof
Date&&typeof b!=="undefined"&&b instanceof Date?c.ui.rangeSlider.prototype.bounds.apply(this,[a.valueOf(),b.valueOf()]):c.ui.rangeSlider.prototype.bounds.apply(this,this._toArray(arguments));return{min:new Date(d.min),max:new Date(d.max)}},_toArray:function(a){return Array.prototype.slice.call(a)}})})(jQuery);
