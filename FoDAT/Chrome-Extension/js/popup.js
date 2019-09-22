function save_options(){

	let api_key = $('#api_key').val();

	chrome.storage.sync.set({
		api_key: api_key

	}, ()=> {
		$('body').prepend('<div id="save-msg" class="alert alert-success" role="alert">Modifica salvata!</div>');
		setTimeout(()=>{

			chrome.tabs.query({active: true, currentWindow: true}, (tabs)=> {
				if(tabs[0].url.indexOf('forgeofempires.com/game/index') > -1){
					chrome.tabs.reload(tabs[0].id);
				}
			});
			window.close();
		}, 2000);
	});
}

function restore_options(){
	chrome.storage.sync.get({
		api_key:''
		
	}, (items)=> {
		$('#api_key').val(items.api_key);
	});
}

function avvia(){
	chrome.windows.create({"url": "http://it.forgeofempires.com/", "incognito": true});
}


document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click', save_options);
document.getElementById('avvia').addEventListener('click', avvia);
