 // Function to handle the creation of list items for nested JSON
 function clearResults(){
    const jsonResultsDiv = document.getElementById('jsonResults');
    jsonResultsDiv.innerHTML = ''; // Clear any existing content
 }


function showAlert(alertType, alertText) {
    //'alert-warning', 'alert-success'
    const alertDiv = document.createElement('div');
    alertDiv.classList.add('alert', 'alert-dismissible', 'fade', 'show');
    alertDiv.classList.add(alertType);
    alertDiv.innerHTML = `
    ${alertText}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
`;
    const alertArea = document.getElementById('alertArea');
    alertArea.appendChild(alertDiv);
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);     
}

function confirmDownload() {
    // Validate file selection (you can add additional validation here)
    const fileInput = document.getElementById('urlInput');
    // TODO: Add REGEX url validation
    if (false) {
        showAlert('alert-warning', "Error: Please select a valid url");
        return;
    }
    // If URL is valid
    showAlert('alert-success', "Success: Processing file");
    // Send an HTTP request to the specified endpoint (adjust the URL as needed)
    const urlToDownload = document.getElementById("urlInput").value
    const bodyToSend = JSON.stringify({ url: urlToDownload });
    fetch('/api/ytdownloadsplit', {
        method: 'POST',
        body: bodyToSend,
        headers: {
            'Content-Type': 'application/json'
        },        
    })
    .then(response => {
        if (response.ok) {
        
            return; // TODO return file and let the user download it
        } else {
            showAlert('alert-error', "Error: Error downloading and returning the PDF");
            return;
        }
    })
    
    .catch(error => {
        console.error('Error:', error);
    });
}