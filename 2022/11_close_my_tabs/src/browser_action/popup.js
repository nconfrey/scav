// always waits the document to be loaded when shown
document.addEventListener('DOMContentLoaded', function() {

  // opens a communication between scripts
  var port = chrome.runtime.connect();

  // listens to the click of the button into the popup content
  document.getElementById('closeTabButton').addEventListener('click', function() {

    // sends a message throw the communication port
    port.postMessage({
      'from': 'popup',
      'action': 'closeTab'
    });
  });
});
