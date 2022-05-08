// opens a communication port
chrome.runtime.onConnect.addListener(function(port) {

  // listen for every message passing throw it
  port.onMessage.addListener(function(o) {

    // if the message comes from the popup
    if (o.from && o.from === 'popup' && o.action === 'closeTab') {
      closeRandomTab();
    }
  });
});

function closeRandomTab() {
  chrome.tabs.query({}, function(tab_list) {
    const randomIdx = Math.floor(Math.random() * tab_list.length);
    const randomTab = tab_list[randomIdx];
    chrome.tabs.remove(randomTab['id']);
  })
}

function autoRandomCloseTabs() {
    closeRandomTab();
    var min = 5, max = 60; // configure this for number of seconds to randomly choose between
    var rand = Math.floor(Math.random() * (max - min + 1) + min); //Generate Random number between min - max
    setTimeout(autoRandomCloseTabs, rand * 1000);
}

autoRandomCloseTabs();
