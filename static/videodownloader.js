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
    })
    .then(response => {
        if (response.ok) {
            //alert('File uploaded successfully!');
            return response.json(); // Parse the response as JSON
            // Handle any additional actions (e.g., redirect, display success message)
        } else {
            alert('Error uploading file. Please try again.');
        }
    })
    .then(jsonData => {
        const jsonResultsDiv = document.getElementById('jsonResults');
        jsonResultsDiv.innerHTML = ''; // Clear any existing content
        // Create an unordered list to display the keys and values
        const ul = document.createElement('div');
        ul.classList.add('list-group')
        createListItems(jsonData, ul); // Start the recursive function call
    
        // Append the list to the div
        jsonResultsDiv.appendChild(ul);
    })         
    .catch(error => {
        console.error('Error:', error);
    });
}