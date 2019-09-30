chrome.storage.sync.get({
    api_key: ''

}, (items) => {
	let manifestData = chrome.runtime.getManifest(),
		v = manifestData.version;

	let code = "let api_key='" + (items.api_key || "0") + "',extID='"+ chrome.runtime.id + "',v='" + v + "'",
		script = document.createElement('script');

	script.id = 'InitData';
	script.innerText = code;
	(document.head || document.documentElement).appendChild(script);

	let s = [
		'ant'
	];

	for(let i in s){
		if(s.hasOwnProperty(i)){
			let sc = document.createElement('script');
			sc.src = chrome.extension.getURL('js/web/' + s[i] + '.js?v=' + v);
			sc.id = s[i] + '-script';
			sc.onload = function(){
				this.remove();
			};
			(document.head || document.documentElement).appendChild(sc);
		}
	}
});

