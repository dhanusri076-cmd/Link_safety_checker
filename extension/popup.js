document.addEventListener('DOMContentLoaded', function() {
    const statusElement = document.getElementById('status');
    const reasonElement = document.getElementById('reason');

    // 1. Get the current active tab's URL
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        let currentTab = tabs[0];
        let url = currentTab.url;

        // Display "Checking..." while we wait for the server
        statusElement.innerText = "Checking safety...";
        statusElement.style.color = "orange";

        // 2. Send the URL to your Flask Backend
        fetch('http://localhost:5000/check_link', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            // 3. Update the UI based on server response
            if (data.status === "danger") {
                statusElement.innerText = "⚠️ DANGER DETECTED";
                statusElement.style.color = "red";
                reasonElement.innerText = data.reason;
            } else {
                statusElement.innerText = "✅ SITE SECURE";
                statusElement.style.color = "green";
                reasonElement.innerText = "No immediate scam indicators found.";
            }
        })
        .catch(error => {
            statusElement.innerText = "Server Error";
            statusElement.style.color = "gray";
            reasonElement.innerText = "Make sure your Python server is running.";
            console.error('Error:', error);
        });
    });
});
