chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && !tab.url.startsWith('chrome://')) {

    const url = new URL(tab.url);
    const domain = url.hostname;

    fetch(`http://localhost:5000/check_link?domain=${domain}`)
      .then(response => response.json())
      .then(data => {
        if (data.is_malicious) {
          // This object MUST have type, title, and message
          chrome.notifications.create("safety-alert", {
            type: 'basic', // Even if it's missing, keep the property
            iconUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
            title: 'Link Safety Checker',
            message: '🚨 DANGER: This site was registered today! It may be a scam.',
          });
        }
      })
      .catch(err => console.log("Server error:", err));
  }
});
