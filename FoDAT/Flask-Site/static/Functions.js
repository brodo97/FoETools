function getOff(val) {
    let off = 0;
    if (Math.max.apply(null, val)-Math.min.apply(null, val) !== 0) {
        off = parseInt((Math.max.apply(null, val)-Math.min.apply(null, val))*0.03);
    }else{
        off = parseInt(Math.max.apply(null, val)*0.03);
    }
    if (off === 0) {
        off = 1;
    }
    return off;
}

function getMin(val){
    return (Math.min.apply(null, val)-getOff(val)>0 ? Math.min.apply(null, val)-getOff(val) : 0);
}

function getMax(val){
    return Math.max.apply(null, val)+getOff(val);
}

function initActionBtn(l, btn){
	if (l.search === "?detailed") {
		btn.innerHTML = "<i class=\"material-icons\">remove</i>";
		btn.href = l.pathname;
		btn.title = "Riduci dettagli";
	}else{
		btn.innerHTML = "<i class=\"material-icons\">add</i>";
		btn.href = l.pathname + "?detailed";
		btn.title = "Aumenta dettagli";
	}
}