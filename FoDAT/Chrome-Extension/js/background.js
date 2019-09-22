/*chrome.runtime.onInstalled.addListener(() => {
	let version = chrome.app.getDetails().version;

	chrome.tabs.query({active: true, currentWindow: true}, (tabs)=> {
		if(tabs[0].url.indexOf('forgeofempires.com/game/index') > -1){
			if(!isDevMode()){
				chrome.tabs.reload(tabs[0].id);
			}
		}
	});
});

function isDevMode()
{
	return !('update_url' in chrome.runtime.getManifest());
}
*/
let popupWindowId = 0;

chrome.runtime.onMessageExternal.addListener((request) => {
	if (request.type === 'message') {
		let t = request.time,
			opt = {
			type: "basic",
			title: request.title,
			message: request.msg,
			iconUrl: "images/app48.png"
		};

		chrome.notifications.create('', opt, (id)=> {
			setTimeout(()=> {chrome.notifications.clear(id)}, t);
		});

	} else if(request.type === 'storeData'){
		chrome.storage.local.set({ [request.key] : request.data });
	}
});
