document.addEventListener("DOMContentLoaded", function(){
	localStorage.setItem('current_world', window.location.hostname.split('.')[0]);

	let jui = document.createElement('script');
	jui.src = 'chrome-extension://' + extID +  '/vendor/jQuery/jquery-ui.min.js';
	jui.id = 'clipboard-script';
	jui.onload = function(){
		this.remove();
	};
	(document.head || document.documentElement).appendChild(jui);

});


let BuildingNamesi18n = false,
	Conversations = [],
	T_GE_Invest = [],
	Alert_Avvisato = false,
	ResourcesQuantity = false,
	Resources = undefined,
	Sent = [],
	user_id = 0,
	user_name = "",
	clan_id = 0,
	clan_name = "";

(function() {
	let XHR = XMLHttpRequest.prototype,
		open = XHR.open,
		send = XHR.send;


	XHR.open = function(method, url){
		this._method = method;
		this._url = url;
		return open.apply(this, arguments);
	};

	XHR.send = function(postData){

		this.addEventListener('load', function(){
			if(this._url.indexOf("metadata?id=city_entities") > -1 && BuildingNamesi18n === false){
				BuildingNamesi18n = [];
				MainParser.loadJSON(this._url,function(r) {
					let j = JSON.parse(r);

					for (let i in j){
						if (j.hasOwnProperty(i)){
							BuildingNamesi18n[j[i]['asset_id']] = j[i]['name'];
						}
					}
				});
			}

			if(this._url.indexOf("metadata?id=unit_types") > -1) {
				try {
					let d = JSON.parse(this.responseText);
					MainParser.sendJSON(d, "army_definitions");
				} catch (err) {
					console.error(err, this._url, this.responseText);
				}
			}
			

			if(this._url.indexOf("game/json?h=") > -1){
				let d = JSON.parse(this.responseText);
				
				//console.log(d);
				
				let StartupService = d.find(obj => {
					return obj.requestClass === 'StartupService' && obj.requestMethod === 'getData';
				});

				let RankingService = d.find(obj => {
					return obj.requestClass === 'RankingService' && obj.requestMethod === 'newRank';
				});

				if(StartupService !== undefined && RankingService !== undefined){
					MainParser.StartUp([StartupService, RankingService]);
				}

				let ConversationService = d.find(obj => {
					return (obj.requestClass === 'ConversationService' && obj.requestMethod === 'getOverview') || (obj.requestClass === 'ConversationService' && obj.requestMethod === 'getTeasers');
				});

				if(ConversationService !== undefined){
					MainParser.setConversations(ConversationService['responseData']);
				}

				let GEInvests = d.find(obj => {
					return obj.requestClass === 'GreatBuildingsService' && obj.requestMethod === 'getContributions'
				});

				if(GEInvests !== undefined){
					T_GE_Invest = GEInvests;
				}

				let ResourcesNames = d.find(obj => {
					return obj.requestClass === 'ResourceService' && obj.requestMethod === 'getResourceDefinitions';
				});

				let ResourcesTmp = d.find(obj => {
					return obj.requestClass === 'ResourceService' && obj.requestMethod === 'getPlayerResources';
				});

				if (ResourcesTmp !== undefined) {
					Resources = ResourcesTmp;
				}

				let Depostits = d.find(obj => {
					return obj.requestClass === 'CampaignService' && obj.requestMethod === 'getDeposits';
				});

				if(ResourcesTmp !== undefined && ResourcesNames !== undefined && Depostits !== undefined){
					MainParser.getResourcesQuantity(ResourcesNames['responseData'], Resources['responseData']['resources'], Depostits['responseData']['states']);
					MainParser.sendJSON(ResourcesNames['responseData'], "definitions");
					MainParser.sendJSON(Resources['responseData']['resources'], "resources");
				}

				let Inventory = d.find(obj => {
					return obj.requestClass === 'InventoryService' && obj.requestMethod === 'getItems';
				});

				if (Inventory !== undefined) {
					MainParser.sendJSON(Inventory['responseData'], "inventory");
				}

				let Army = d.find(obj => {
					return obj.requestClass === 'ArmyUnitManagementService' && obj.requestMethod === 'getArmyInfo';
				});

				if (Army !== undefined) {
					MainParser.sendJSON(Army['responseData'], "army");
				}

				let GuildTreasure = d.find(obj => {
					return obj.requestClass === 'ClanService' && obj.requestMethod === 'getTreasury';
				});

				if (GuildTreasure !== undefined && clan_id !== 0) {
					MainParser.sendJSON(GuildTreasure['responseData']['resources'], "guild_resources");
				}
			}
		});
		
		return send.apply(this, arguments);
	};
})();

MainParser = {
	getResourcesQuantity: (names, quantity, deposits)=> {
		ResourcesQuantity = [];
		let GroupResourcesByAge = [];
		for (let i in names){
			if (names[i]['era'] !== 'AllAgeNoAge' && 'goodsProduceable' in names[i]['abilities'] && names[i]['id'] in quantity){
				ResourcesQuantity[names[i]['id']] = [names[i]['name'], quantity[names[i]['id']]];
				if (names[i]['era'] in GroupResourcesByAge) {
					GroupResourcesByAge[names[i]['era']].push([names[i], quantity[names[i]['id']]]);
				}else{
					GroupResourcesByAge[names[i]['era']] = [[names[i], quantity[names[i]['id']]]];
				}
			}
		}
		for (let era in GroupResourcesByAge){
			if (GroupResourcesByAge[era].length === 5){
				let goods = [];
				let boost = [];
				for (good in GroupResourcesByAge[era]){
					let good_deposit = GroupResourcesByAge[era][good][0]['abilities']['goodsProduceable']['deposit'];
					if (good_deposit in deposits && deposits[good_deposit] === 2){
						boost.push(GroupResourcesByAge[era][good][0]['id']);
					}else{
						goods.push(GroupResourcesByAge[era][good][0]['id']);
					}
				}
				console.info("\n" + era);
				if (goods.length === 3 && boost.length === 2){
					let g1 = [goods[0], ResourcesQuantity[goods[0]]];
					let g2 = [goods[1], ResourcesQuantity[goods[1]]];
					let g3 = [goods[2], ResourcesQuantity[goods[2]]];
					let d1 = [boost[0], ResourcesQuantity[boost[0]]];
					let d2 = [boost[1], ResourcesQuantity[boost[1]]];

					let avg = (g1[1][1] + g2[1][1] + g3[1][1] + d1[1][1] + d2[1][1])/5;
					let dep1 = avg - d1[1][1];
					let dep2 = avg - d2[1][1];
					let res1 = avg - g1[1][1];
					let res2 = avg - g2[1][1];
					let res3 = avg - g3[1][1];

					let ratio1 = 100 / -(dep1 + dep2) * -dep1;
					let ratio2 = 100 / -(dep1 + dep2) * -dep2;

					let tradeD1R1 = parseInt(ratio1 / 100 * res1);
					let tradeD1R2 = parseInt(ratio1 / 100 * res2);
					let tradeD1R3 = parseInt(ratio1 / 100 * res3);
					let tradeD2R1 = parseInt(ratio2 / 100 * res1);
					let tradeD2R2 = parseInt(ratio2 / 100 * res2);
					let tradeD2R3 = parseInt(ratio2 / 100 * res3);

					console.info("\t" + d1[1][0] + " -> " + tradeD1R1 + " -> " + g1[1][0]);
					console.info("\t" + d1[1][0] + " -> " + tradeD1R2 + " -> " + g2[1][0]);
					console.info("\t" + d1[1][0] + " -> " + tradeD1R3 + " -> " + g3[1][0]);
					console.info("\t" + d2[1][0] + " -> " + tradeD2R1 + " -> " + g1[1][0]);
					console.info("\t" + d2[1][0] + " -> " + tradeD2R2 + " -> " + g2[1][0]);
					console.info("\t" + d2[1][0] + " -> " + tradeD2R3 + " -> " + g3[1][0]);
				}else{
					console.info("\tImpossible to balance");
				}
			}
		}
	},

	getAddedDateTime: (hrs, min)=> {

		let time = new Date().getTime(),
			h = hrs || 0,
			m = min || 0;
			newTime = time + (1000*60*m) + (1000*60*60*h),
			newDate = new Date(newTime);

		let FutureDate = newDate.getTime();

		return FutureDate;
	},

	getCurrentDateTime: ()=> {
		return new Date().getTime();
	},

	compareTime: (actual, storage)=> {

		if(storage === null){
			return true;
		} else if(actual > storage){
			return true;
		} else if(storage > actual){

			let diff = Math.abs(actual - storage),
				timeDiff = new Date(diff);

			let hh = Math.floor(timeDiff / 1000 / 60 / 60);
			if(hh < 10) {
				hh = '0' + hh;
			}
			timeDiff -= hh * 1000 * 60 * 60;

			let mm = Math.floor(timeDiff / 1000 / 60);
			if(mm < 10) {
				mm = '0' + mm;
			}
			timeDiff -= mm * 1000 * 60;

			let ss = Math.floor(timeDiff / 1000);
			if(ss < 10) {
				ss = '0' + ss;
			}

			return mm + "min und " + ss + 's';
		}
	},

	StartUp: (d)=> {
		user_id = d[0]['responseData']['user_data']['player_id'];
		user_name = d[0]['responseData']['user_data']['user_name'];
		clan_id = d[0]['responseData']['user_data']['clan_id'];
		clan_name = d[0]['responseData']['user_data']['clan_name'];
		score = 0;
		rank = d[1]['responseData']['rank'];

		for (let i in d[0]['responseData']['socialbar_list']){
			if (d[0]['responseData']['socialbar_list'][i]['is_self']){
				score = d[0]['responseData']['socialbar_list'][i]['score'];
			}
		}

		MainParser.sendJSON({"user_id": user_id, "user_name": user_name, "clan_id": clan_id, "clan_name": clan_name, "score": score, "position": rank}, "userdata");

		chrome.runtime.sendMessage(extID, {
			type: 'storeData',
			key: 'user_name',
			data: user_name
		});
		localStorage.setItem('user_name', user_name);
	},

	setConversations: (d)=> {

		// GildenChat
		if(d['clanTeaser'] !== undefined && Conversations.filter((obj)=> (obj.id === d['clanTeaser']['id'])).length === 0){
			Conversations.push({
				id: d['clanTeaser']['id'],
				title: d['clanTeaser']['title']
			});
		}

		if(d['teasers'] !== undefined){
			// die anderen Chats
			for(let k in d['teasers']){

				if(d['teasers'].hasOwnProperty(k)){

					if(Conversations.filter((obj)=> (obj.id === d['teasers'][k]['id'])).length === 0){
						Conversations.push({
							id: d['teasers'][k]['id'],
							title: d['teasers'][k]['title']
						});
					}
				}
			}
		}

		if(d[0] !== undefined && d[0].length > 0){

			for(let k in d){
				if(d.hasOwnProperty(k)){
					if(Conversations.filter((obj)=> (obj.id === d[k]['id'])).length === 0){
						Conversations.push({
							id: d[k]['id'],
							title: d[k]['title']
						});
					}
				}
			}
		}
	},

	loadJSON: (url, callback)=> {

		let xobj = new XMLHttpRequest();
		xobj.overrideMimeType("application/json");
		xobj.open('GET', url, true);
		xobj.onreadystatechange = function () {
			if (xobj.readyState == 4 && xobj.status == "200") {
				callback(xobj.responseText);
			}
		};
		xobj.send(null);
	}
};
