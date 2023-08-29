chrome.runtime.onMessage.addListener((function(t, e, n) {
	"startAudio" == t.data && guruContent.createAudio()
}));
class Content {
	constructor() {
		this.initStorage(), this.clearBtn = null, this.isBtn = null
	}
	initStorage() {
		chrome.storage.local.get(["floatbtn"], (t => {
			this.isBtn = t.floatbtn, this.createBtn()
		})), chrome.storage.local.get(["shortCuts"], (t => {
			this.isShortCuts = t.shortCuts, this.isShortCuts
		}))
	}
	createBtn() {
		const t = document.createElement("img");
		t.className = "inserted-btn mtz", t.src = chrome.runtime.getURL(
				"images/icon_main.svg"), t.alt = "Clear Button", t.addEventListener(
				"click", this.handleClearBtn.bind(this)), this.clearBtn = t,
			document.body.appendChild(t)
	}
	handleClearBtn(t) {
		t.target.style.transform = "scale(0.5)", setTimeout((() => {
			t.target.style.transform = "scale(1)"
		}), 400), chrome.runtime.sendMessage({
			action: "clearBtn"
		})
	}
	initListeners() {
		chrome.storage.onChanged.addListener((t => {
			t.hasOwnProperty("floatbtn") && (this.isBtn = t.floatbtn
				.newValue, this.checkBtnInserting())
		}))
	}
	deleteBtn() {
		this.clearBtn.remove(), this.clearBtn = null
	}
	createAudio() {
		const t = chrome.runtime.getURL("audios/accomplished.mp3");
		let e = new Audio(t);
		e.id = "audio", e.autoplay = !0, document.body.appendChild(e)
	}
}
const guruContent = new Content;