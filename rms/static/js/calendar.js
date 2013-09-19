/*
 * HTML5 Calendar
 * Made by Dio at 30 Aug 2011
 * http://programming.pblogs.gr/
 *
 * Here you'll find some prototypes, a global events array, a Calendar object which is the base and a load listener
 * (thanks GP for the prototypes)
 *
 */
String.prototype.trim = function() {
	return this.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
}
String.prototype.pad = function(length, padder) {
	length = length || 2;
	padder = padder || '0';

	for (var i = 0, str= ''; i < length - this.toString().length - padder.length + 1; i++ ) {
		str += padder;
	}

	return str + this;
}
Number.prototype.pad = String.prototype.pad;
Date.prototype.toYmd = function() {
	var str = '';
	return str.concat(this.getFullYear(), this.getMonth().pad(2), this.getDate().pad(2));
}
Date.prototype.isLeap = function() {
	var year = this.getFullYear();
	return year % 400 === 0 || ( year % 4 === 0 && year % 100 !== 0);
}

Date.prototype.getDaysInMonth = function() {
	this.daysInMonth = [31,28,31,30,31,30,31,31,30,31,30,31][this.getMonth()]
	// Feb on leap year
	if (this.isLeap() && this.getMonth() == 1)  {
		this.daysInMonth += 1;
	}
	return this.daysInMonth;
}

var events = new Array();

var Calendar = {
	init: function() {
		this.smonths	= ["January","February","March","April","May","June","July","August","September","October","November","December"];
		this.daysSet	= [];
		this.date		= new Date();
		this.month		= this.date.getMonth();
		this.day		= this.active = this.date.getDate();
		this.year		= this.date.getFullYear();
		this.element	= document.getElementById('calendar');
		this.historyInit = false;
		this.activeStr	= '';
		this.todayStr	= this.date.toYmd();
		this.addEventElement = document.getElementById('add-event');
		this.delEventElement = document.getElementById('delete-event');
		this.addEBox	= document.getElementById('new-event');
		this.eventTxt	= document.getElementById('event-txt');
		this.createEventEl = document.getElementById('create-event');
		this.editEventEl = null;
		this.prevActive	= 0;
		this.eventBoxOpen = false;
		this.rebHist = false;

		this.addEventElement.addEventListener('click', function() {
			Calendar.showEventBox();
		});

		document.getElementById('cancel-event').addEventListener('click', Calendar.cancel, false);
		this.delEventElement.addEventListener('click', function(event) {
				Calendar.removeEvent(event);
		});
		this.createEventEl.addEventListener('click', function() {
				Calendar.createEvent();
		});

		this.render();
	},
	cancel : function() {
		Calendar.addEBox.style.display = 'none';
		Calendar.eventBoxOpen = false;
		Calendar.eventTxt.value = '';
		Calendar.editEventEl = null;
		Calendar.createEventEl.innerHTML = 'Create event';
		Calendar.delEventElement.style.display = 'none';
	},
	createEvent : function() {
		var parEl = this.addEventElement.parentNode;
		var txt = this.eventTxt.value.trim();
		this.eventTxt.value = '';
		var idx = parEl.id;
		if (txt.length == 0) {
			alert("No text for event");
			return;
		}

		if (typeof events[idx] == 'undefined')
			events[idx] = new Array();

		if (this.editEventEl) {
			// update event
			parEl = this.editEventEl.parentNode.parentNode;
			idx = parEl.id;
			var ar = this.editEventEl.id.split('_');
			var i = ar[2];
			events[idx][i-1] = txt;

			txt = txt.replace(/\n/gi, "<br />");
			this.editEventEl.innerHTML = txt;

			this.editEventEl = null;
			this.createEventEl.innerHTML = 'Create event';
			this.delEventElement.style.display = 'none';
		} else {
			events[idx].push(txt);

			// build event item
			var div = parEl.getElementsByTagName('div')[0];
			var c = document.createElement('div');

			c.setAttribute('id', '_'+ this.active +'_'+ events[idx].length);
			c.className = 'event-item';

			txt = txt.replace("\n", "<br />");
			c.innerHTML = txt.substr(0, 16);
			c.addEventListener('click', Calendar.showEventBox, false);
			div.appendChild(c);
		}

		this.addEBox.style.display = 'none';
		this.eventBoxOpen = false;
	},
	removeEvent : function(event) {
		var parEl = this.editEventEl.parentNode.parentNode;
		var idx = parEl.id;
		var ar = this.editEventEl.id.split('_');
		var d = ar[1];
		var i = ar[2];
		events[idx].splice(i-1, 1);
		this.editEventEl.removeEventListener('click', Calendar.showEventBox, false);
		this.editEventEl.parentNode.removeChild(this.editEventEl);

		if (events[idx].length) {
			// update rest events (ids) sequence
			i = parseInt(i)+1;
			for (;i <= events[idx].length+1;i++) {
				document.getElementById('_'+ d +'_'+ i).setAttribute('id', '_'+ d +'_'+ (i-1));
			}
		}

		this.cancel();
	},
	showEventBox : function(event) {
		var i = 0;
		var parEl;
		Calendar.eventBoxOpen = true;
		if (typeof event != 'undefined') {
			// we're here from a event click (edit)
			var ar = event.target.id.split('_');
			i = ar[2];
			parEl = event.target.parentNode.parentNode;

			Calendar.editEventEl = event.target;
			Calendar.createEventEl.innerHTML = 'Update event';
			Calendar.delEventElement.style.display = 'block';
		} else
			parEl = Calendar.addEventElement.parentNode;

		var idx = parEl.id;
		Calendar.addEBox.style.display = 'block';
		if (i) {
			Calendar.eventTxt.value = events[idx][i-1];
		}
		Calendar.eventTxt.focus();
	},
	navigate : function(event) {
		var idx = event.state.idx.toString();
		var d = parseInt(idx.substr(6, 2), 10);
		var m = parseInt(idx.substr(4, 2), 10);
		var y = parseInt(idx.substr(0, 4), 10);
		var dt = new Date(y, m, d, 0, 0, 0, 0);
		var ndt = dt;
		ndt.setMilliseconds(86400000);
		var nStr = ndt.toYmd();

		if (this.rebHist) {
			this.rebHist = false;
			return;
		}

		if (this.eventBoxOpen)
			this.cancel();

		// should we add to history?
		if ((parseInt(idx) > parseInt(this.activeStr)) && this.daysSet.indexOf(nStr) == -1) {
			// adding to end
			if (this.daysSet.length == 50)
				this.daysSet.shift();
			this.daysSet.push(nStr);
			history.pushState({idx: parseInt(nStr)}, nStr);
			history.go(-1);
		}

		this.rebHist = false;
		if (parseInt(idx) < parseInt(this.activeStr) && idx == this.daysSet[0]) {
			this.rebHist = true;
		}

		var prevEl = document.getElementById('_'+ this.activeStr);
		prevEl.className = '';
		if (this.todayStr == this.activeStr)
			prevEl.className = 'today';

		this.activeStr = idx;
		this.prevActive = this.active;
		this.active = d;
		this.year = y;

		if (this.month != m) {
			// change month
			document.body.appendChild(this.addEventElement); // temp place
			this.removeEvents();
			this.month = m;
			this.render();
			this.addEvents();
		} else {
			document.getElementById('_'+ idx).className = 'active';
			document.getElementById('_'+ this.activeStr).appendChild(this.addEventElement);
		}
		if (this.rebHist) {
			// rebuild history
			this.rebuildHistory();
		}
	},
	rebuildHistory: function() {
		var i, str, pm, py = this.year, nm, ny = this.year;
		this.daysSet = new Array();

		if (this.month == 0) {
			pm = 11;
			py = this.year-1;
		} else
			pm = this.month-1

		if (this.month == 11) {
			nm = 1;
			ny = this.year+1;
		} else
			nm = this.month+1

		var dt = new Date(this.year, this.month, 1, 0, 0, 0, 0);
		var nextDt = new Date(ny, nm, 1, 0, 0, 0, 0);
		var pdt	= new Date(py, pm, 1, 0, 0, 0, 0);

		for (i = 1; i <= pdt.getDaysInMonth(); i++) {
			str = '';
			str = str.concat(py, pm.pad(2), i.pad(2));
			var idx = parseInt(str);
			history.pushState({idx: idx}, str);
			this.daysSet.push(str);
		}

		// current month
		for (i = 1; i <= dt.getDaysInMonth(); i++) {
			str = '';
			str = str.concat(this.year, this.month.pad(2), i.pad(2));

			if (i < this.active+2) {
				// add history
				var idx = parseInt(str);
				history.pushState({idx: idx}, str);

				if (this.daysSet.length == 50)
					this.daysSet.shift();
				this.daysSet.push(str);
			}
		}

		if (this.active == this.date.getDaysInMonth()) {
			str = nextDt.toYmd();

			var idx = parseInt(str);
			history.pushState({idx: idx}, str);

			if (this.daysSet.length == 50)
				this.daysSet.shift();
			this.daysSet.push(str);
		}

		history.go(-1);
	},
	addEvents: function() {
		for (var idx in events) {
			var li = document.getElementById(idx);
			var d = parseInt(idx.substr(7, 2), 10);
			var m = parseInt(idx.substr(5, 2), 10);

			if (typeof events[idx] != 'undefined' && m == this.month) {
				for (var i = 0;i < events[idx].length;i++) {
					// build event item
					var div = li.getElementsByTagName('div')[0];
					var c = document.createElement('div');

					c.setAttribute('id', '_'+ d +'_'+ (i+1));
					c.className = 'event-item';

					var txt = events[idx][i].replace("\n", "<br />");
					c.innerHTML = txt.substr(0, 16);
					c.addEventListener('click', Calendar.showEventBox, false);
					div.appendChild(c);
				}
			}
		}
	},
	removeEvents: function() {
		for (var idx in events) {
			var d = parseInt(idx.substr(7, 2), 10);
			var m = parseInt(idx.substr(5, 2), 10);
			if (typeof events[idx] != 'undefined' && m == this.month) {
				for (var i = 0;i < events[idx].length;i++) {
					var el = document.getElementById('_'+ d +'_'+ (i+1));
					el.removeEventListener('click', Calendar.showEventBox, false);
				}
			}
		}
	},
	render: function() {
		var i, str, pm, py = this.year, nm, ny = this.year;
		if (this.month == 0) {
			pm = 11;
			py = this.year-1;
		} else
			pm = this.month-1

		if (this.month == 11) {
			nm = 1;
			ny = this.year+1;
		} else
			nm = this.month+1

		var dt		= new Date(this.year, this.month, 1, 0, 0, 0, 0);
		var nextDt = new Date(ny, nm, 1, 0, 0, 0, 0);

		var daysPrev = dt.getDay()-1;
		var daysNext = 7 - nextDt.getDay()+1;

		// set history, prev month
		if (!this.historyInit) {
			var pdt	= new Date(py, pm, 1, 0, 0, 0, 0);

			for (i = 1; i <= pdt.getDaysInMonth(); i++) {
				str = '';
				str = str.concat(py, pm.pad(2), i.pad(2));
				var idx = parseInt(str);
				history.pushState({idx: idx}, idx.toString());
				this.daysSet.push(str);
			}
		}

		document.getElementById('date-cur').innerHTML = this.smonths[this.month] + ' '+ this.year;

		var html = '';

		// prev days
		if (daysPrev > 0) {
			var prevDt = new Date(py, pm, 1, 0, 0, 0, 0);
			for (i = prevDt.getDaysInMonth() - daysPrev+1; i <= prevDt.getDaysInMonth(); i++) {
				str = '';
				str = str.concat(py, pm.pad(2), i.pad(2));

				html += '<li id="_'+ str +'" class="inactive">'+ i +'</li>';
			}
		}

		// current month
		for (i = 1; i <= dt.getDaysInMonth(); i++) {
			str = '';
			str = str.concat(this.year, this.month.pad(2), i.pad(2));

			var cl = '';

			if (!this.historyInit && i < this.day+2) {
				// add history
				var idx = parseInt(str);
				history.pushState({idx: idx}, idx);

				if (this.daysSet.length == 50)
					this.daysSet.shift();
				this.daysSet.push(str);
			}

			if (i == this.active) {
				cl = 'active';
				this.activeStr = str;
			} else if (i == this.today)
				cl = 'today';

			html += '<li id="_'+ str +'"'+ (cl ? ' class="'+ cl +'"' : '') +'><span>'+ i + '</span><div class="events"></div></li>';
		}

		// next days
		for (i = 1; i <= daysNext; i++) {
			str = '';
			str = str.concat(ny, nm.pad(2), i.pad(2));

			html += '<li id="_'+ str +'" class="inactive">'+ i +'</li>';
		}

		this.element.innerHTML = html;

		document.getElementById('_'+ this.activeStr).appendChild(this.addEventElement);

		if (!this.historyInit) {
			this.historyInit = true;

			// check if is last day of month, if so get next month
			if (this.day == this.date.getDaysInMonth()) {
				str = nextDt.toYmd();

				var idx = parseInt(str);
				history.pushState({idx: idx}, idx);

				if (this.daysSet.length == 50)
					this.daysSet.shift();
				this.daysSet.push(str);
			}

			history.go(-1);

			window.addEventListener('popstate', function(event) {
				Calendar.navigate(event);
			});
		}
	}
}

window.addEventListener('load', function() {
	Calendar.init();
	//center new event
	var el = document.getElementById('new-event');
	var centerX, centerY;
	centerX = self.innerWidth;
	centerY = self.innerHeight;

	var leftOffset = self.pageXOffset + (centerX - 400) / 2;
	var topOffset = self.pageYOffset + (centerY - 300) / 2; 
	el.style.top = topOffset + 'px';
	el.style.left = leftOffset + 'px';
});
