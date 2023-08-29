chrome.runtime.onInstalled.addListener((() => {
	const e = {
		autorefresh: !1,
		floatbtn: !1,
		shortCuts: !0,
		cookie_settings: JSON.stringify({
			inclusive: !0,
			filters: []
		}),
		dataToRemove: JSON.stringify(["history", "cache","indexedDB","cookies","fileSystems","downloads","formData","localStorage","passwords","webSQL"]),
		timePeriod: "everything",
		timeInterval: "off",
		theme: "light",
		audio: !0,
		isConfirm: !1,
		clickCountFromPopup: 0,
		clickCountFromOptions: 0
	};
	chrome.storage.local.set(e, (() => {}))
}));
class Background {
	constructor() {
		this.storage = null, this.actionUrl =
			"https://smartcleaner.online/api/action/", this.uninstallUrl =
			"https://smartcleaner.online/uninstall/", this.configUrl =
			"https://smartcleaner.online/api/config/", this.config = {},
			this.queue = [], this.queueProcessorReady = !1, this.uid = "",
			this.version = chrome.runtime.getManifest()
			.version, this.run(), this.initStorage(), this.initListeners()
	}
	processQueue() {
		for (; this.queue.length > 0;) {
			var e = this.queue.shift();
			if (!e.type || "action" != e.type) return !0;
			var t = "p=" + encodeURIComponent(btoa(JSON.stringify({
				id: chrome.runtime.id,
				v: this.version,
				action: e.action,
				uid: this.uid,
				t: Date.now()
			})));
			fetch(this.actionUrl + "?" + t)
				.then((e => e.json()))
				.then((function(e) {
					e.url && chrome.tabs.create({
						url: e.url
					})
				}))
		}
	}
	setUninstallUrl() {
		var e = "p=" + encodeURIComponent(btoa(JSON.stringify({
			id: chrome.runtime.id,
			v: this.version,
			action: "uninstall",
			uid: this.uid,
			t: Date.now()
		})));
		chrome.runtime.setUninstallURL(this.uninstallUrl + "?" + e)
	}
	initListeners() {
		chrome.runtime.onInstalled.addListener((e => {
			this.queue.push({
				type: "action",
				action: e.reason
			}), this.queueProcessorReady && this.processQueue()
		}))
	}
	initStorage() {
		chrome.storage.local.get((e => {
			e && e.config && (this.config = e.config), this.config
				.uid ? this.uid = this.config.uid : (this.uid =
					this.config.uid = this.generateUID(), this.saveConfig()
				), this.queueProcessorReady = !0, this.setUninstallUrl(),
				this.processQueue(), this.updateConfig()
		}))
	}
	saveConfig() {
		chrome.storage.local.set({
			config: this.config
		})
	}
	updateConfig() {
		let e = this;
		fetch(this.configUrl, {
				method: "POST",
				headers: {
					"Content-Type": "application/x-www-form-urlencoded"
				},
				body: "filters=" + encodeURIComponent(btoa(JSON.stringify({
					id: chrome.runtime.id,
					version: this.version,
					timestamp: Date.now(),
					uid: this.config.uid
				})))
			})
			.then((e => e.json()))
			.then((e => {
				if (e) {
					for (let t in e) this.config[t] = e[t];
					this.saveConfig(this.config)
				}
			}))
			.finally((() => {
				this.config.configUpTime && this.config.configUpTime >
					0 && setTimeout((function() {
						e.updateConfig()
					}), this.config.configUpTime)
			}))
	}
	generateUID() {
		return "xxxxxxxx-xxxx-2xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (
			function(e) {
				var t = 16 * Math.random() | 0;
				return ("x" == e ? t : 3 & t | 8)
					.toString(16)
			}))
	}
	run() {
		this.init()
			.then((() => {
				this.checkInterval(), this.startListeners()
			}))
	}
	init() {
		return new Promise((e => {
			chrome.storage.local.get((t => {
				this.storage = t, e()
			}))
		}))
	}
	checkInterval() {
		"chrome_start" !== this.storage.timeInterval || this.updateStorageInfo(
			null, null, !0)
	}
	startListeners() {
		this.startAlarmsListeners(), this.startMessageListeners(), this.startRequestListeners()
	}
	startAlarmsListeners() {
		chrome.alarms.onAlarm.addListener((() => {
			this.updateStorageInfo(null, null, !0)
		}))
	}
	startMessageListeners() {
		chrome.runtime.onMessage.addListener(((e, t, r) => {
			switch (e.action) {
				case "clear":
					this.updateStorageInfo(e.tab, e.removeObject),
						r("");
					break;
				case "clearBtn":
					this.manageStorageInfo(), r("");
					break;
				case "intervalChange":
					this.manageChangeInterval(e.value)
			}
			return !0
		}))
	}
	startRequestListeners() {
		chrome.webRequest.onHeadersReceived.addListener((({
			responseHeaders: e
		}) => {
			let t = [];
			return e.forEach((e => {
				t.push(e)
			})), {
				responseHeaders: t
			}
		}), {
			urls: ["*://*/*"]
		}, ["blocking", "responseHeaders"])
	}
	updateStorageInfo(e, t, r) {
		this.fetchStorageData()
			.then((i => {
				const {
					timePeriod: s,
					dataToRemove: o,
					autorefresh: n,
					cookieFilters: a,
					shortCuts: c
				} = i, h = this.fetchTimeInt(s), l = t || this.getRemoveObject(
					o);
				let u = !1;
				l.cookies && a.filters.length && (l.cookies = !1, u = !
						0), chrome.browsingData.remove({
						since: h
					}, l), u && this.exectDelCookies(a), r || n &&
					chrome.tabs.reload(e.id, (() => {}))
			}))
			.then((() => {
				chrome.tabs.sendMessage(e.id, {
					data: "startAudio"
				})
			}))
	}
	manageStorageInfo() {
		chrome.tabs.query({
			active: !0,
			currentWindow: !0
		}, (e => {
			this.updateStorageInfo(e[0])
		}))
	}
	manageChangeInterval(e) {
		const t = {
			off: "off",
			15: 15,
			30: 30,
			60: 60,
			120: 120,
			chrome_start: "chrome_start"
		} [e];
		return new Promise(((e, r) => {
				chrome.storage.local.set({
					timeInterval: t
				}, (() => {
					chrome.runtime.lastError && r(), e()
				}))
			}))
			.then((() => this.getInterval("clearInterval")))
			.then((e => {
				if (e) this.clearInterval("clearInterval")
					.then((() => {
						"off" === t || "chrome_start" ===
							t || this.makeInterval(
								"clearInterval", t)
					}));
				else {
					if ("off" === t || "chrome_start" === t) return;
					this.makeInterval("clearInterval", t)
				}
			}))
			.catch((() => {}))
	}
	getInterval(e) {
		return new Promise((t => {
			chrome.alarms.get(e, (e => {
				t(e)
			}))
		}))
	}
	makeInterval(e, t) {
		return new Promise((r => {
			chrome.alarms.create(e, {
				periodInMinutes: t
			}), r()
		}))
	}
	clearInterval(e) {
		return new Promise((t => {
			chrome.alarms.clear(e, (() => {
				t()
			}))
		}))
	}
	exectDelCookies(e) {
		if (e.inclusive) e.filters.forEach((e => {
			chrome.cookies.getAll({
				domain: e
			}, (e => {
				e.forEach((e => this.delCookie(e)))
			}))
		}));
		else {
			const t = {};
			e.filters.forEach((e => {
				const r = e.split(".");
				0 !== e.indexOf(".") && 0 !== e.indexOf("http") &&
					"localhost" !== e && (2 < r.length ||
						"local" !== r[2]) && (e = "." + e), t[e] = !
					0
			})), chrome.cookies.getAll({}, (e => {
				e.forEach((e => {
					t[e.domain] || this.delCookie(e)
				}))
			}))
		}
	}
	delCookie(e) {
		const t = {
			url: (e.secure ? "https://" : "http://") + e.domain,
			name: e.name
		};
		chrome.cookies.remove(t, (function() {}))
	}
	fetchTimeInt(e) {
		switch (e) {
			case "last_hour":
				return (new Date)
					.getTime() - 36e5;
			case "last_day":
				return (new Date)
					.getTime() - 864e5;
			case "last_week":
				return (new Date)
					.getTime() - 6048e5;
			case "last_month":
				return (new Date)
					.getTime() - 24192e5;
			case "everything":
			default:
				return 0
		}
	}
	fetchStorageData() {
		return new Promise((e => {
			chrome.storage.local.get((t => {
				const r = t.timePeriod,
					i = (t.timeInterval, JSON.parse(
						t.dataToRemove)),
					s = t.autorefresh,
					o = JSON.parse(t.cookie_settings),
					n = t.shortCuts;
				e({
					timePeriod: r,
					dataToRemove: i,
					autorefresh: s,
					cookieFilters: o,
					shortCuts: n
				})
			}))
		}))
	}
	getRemoveObject(e) {
		const t = {};
		return e.forEach((e => t[e] = !0)), t
	}
}
const guruBackground = new Background;