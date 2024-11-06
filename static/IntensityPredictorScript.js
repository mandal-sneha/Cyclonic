document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('ip-upload-form');
    const fileInput = document.getElementById('file');
    const loadingIndicator = document.getElementById('ip-loading');
    const resultsContainer = document.getElementById('ip-results');
    const resultsTableBody = document.getElementById('ip-results-body');
    const uploadedImage = document.getElementById('ip-uploaded-image');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            console.log("No file selected.");
            alert("Please select a file first.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        // Show loading indicator and hide previous results
        loadingIndicator.classList.remove('ip-hidden');
        resultsContainer.classList.add('ip-hidden');

        try {
            const response = await fetch('/analyze_cyclone', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                console.error("Network response was not ok. Status:", response.status);
                throw new Error("Network response was not ok");
            }

            const result = await response.json();

            if (result.error) {
                console.error("Server returned an error:", result.error);
                alert(result.error);
            } else {
                // Displaying the uploaded image URL
                uploadedImage.src = result.image_url;
                uploadedImage.alt = "Uploaded Cyclone Image";
                console.log("Uploaded image URL set to:", result.image_url);

                // Clear previous results and populate with new data
                resultsTableBody.innerHTML = '';
                for (const [attribute, value] of Object.entries(result.analysis)) {
                    console.log(`Adding row: ${attribute} - ${value}`);
                    const row = document.createElement('tr');
                    const cellAttr = document.createElement('td');
                    const cellValue = document.createElement('td');
                    cellAttr.textContent = attribute;
                    cellValue.textContent = value;
                    row.appendChild(cellAttr);
                    row.appendChild(cellValue);
                    resultsTableBody.appendChild(row);
                }

                // Show results container
                resultsContainer.classList.remove('ip-hidden');
            }
        } catch (error) {
            console.error("Error occurred while processing the image:", error);
            alert("An error occurred while processing the image. Please try again.");
        } finally {
            // Hide loading indicator
            loadingIndicator.classList.add('ip-hidden');
            console.log("Loading indicator hidden.");
        }
    });
});