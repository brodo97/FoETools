chrome.storage.sync.get({
    api_key: ''

}, (items) => {

	let code = "let api_key='" + (items.api_key || "0") + "',extID='"+ chrome.runtime.id + "'",
		script = document.createElement('script'),
		manifestData = chrome.runtime.getManifest(),
		v = manifestData.version;

	script.id = 'PlayerNumbers';
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

	let cp = document.createElement('script');
	cp.src = chrome.extension.getURL('vendor/clipboard/clipboard.min.js');
	cp.id = 'clipboard-script';
	cp.onload = function(){
		this.remove();
	};
	(document.head || document.documentElement).appendChild(cp);
	
	let style = document.createElement('link');
	style.href = chrome.extension.getURL('css/web/style.css?v=' + v);
	style.id = 'ant-style';
	style.rel = 'stylesheet';
	(document.head || document.documentElement).appendChild(style);
});

