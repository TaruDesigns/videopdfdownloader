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
    // Get and validate URL input
    const urlInput = document.getElementById('urlInput');
    const url = urlInput.value.trim();
    // Regex Validation -> Review this
    if (!url || !url.match(/^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$/)) {
        showAlert('alert-warning', "Error: Please enter a valid YouTube URL");
        return;
    }
    // If URL is valid, show success
    showAlert('alert-success', "Success: Processing file");
    // Show spinner and overlay
    changeButtonProcessing();

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
            return response.blob(); // Convert response to a blob
        } else {
            throw new Error('Error downloading and returning the PDF');
        }
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        // Create a link element and click it to trigger download until I learn to use FileResponse properly
        const a = document.createElement('a');
        a.href = url;
        a.download = 'downloaded_video.pdf'; // TODO: Get filename from request?
        document.body.appendChild(a);
        a.click(); 
        a.remove();
    
        // Hide spinner and overlay
        changeButtonDownload();
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide spinner and overlay
        changeButtonDownload();
        showAlert('alert-error', "Error: " + error.message);
    });
}

function changeButtonProcessing() {
    var button = document.getElementById('downloadButton');
    var spinner = document.createElement('span');
    spinner.classList.add('spinner-border', 'spinner-border-sm');
    spinner.setAttribute('role', 'status');
    spinner.setAttribute('aria-hidden', 'true');
    spinner.id = 'spinnerSpan';
    // Change button text to "Processing"
    button.innerText = ' Processing';
    // Insert the spinner before the text
    button.prepend(spinner);
    // Disable the button
    button.disabled = true;
  }

  function changeButtonDownload() {
    var button = document.getElementById('downloadButton');
    var spinner = document.getElementById('spinnerSpan');
    spinner.remove();
    button.innerText = 'Download';
    button.disabled = false;
  }