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
                uploadedImage.src = result.image_url;
                uploadedImage.alt = "Uploaded Cyclone Image";

                resultsTableBody.innerHTML = '';
                const analysis = result.analysis;
                for (const [attribute, value] of Object.entries(analysis)) {
                    const row = document.createElement('tr');
                    const cellAttr = document.createElement('td');
                    const cellValue = document.createElement('td');
                    cellAttr.textContent = attribute;

                    let formattedValue = value;
                    let unit = '';

                    switch (attribute) {
                        case 'Central Pressure':
                            formattedValue = value.toFixed(0);
                            unit = 'hPa';
                            break;
                        case 'Cyclone Intensity':
                            formattedValue = value.toFixed(1);
                            unit = 'Intensity';
                            break;
                        case 'Eye Diameter':
                            formattedValue = value.toFixed(1);
                            unit = 'km';
                            break;
                        case 'Rainfall Intensity':
                            formattedValue = value.toFixed(1);
                            unit = 'mm/h';
                            break;
                        case 'Sea Surface Temperature':
                            formattedValue = value.toFixed(1);
                            unit = '°C';
                            break;
                        case 'Size (Diameter)':
                            formattedValue = value.toFixed(1);
                            unit = 'km';
                            break;
                    }

                    cellValue.textContent = `${formattedValue} ${unit}`;
                    row.appendChild(cellAttr);
                    row.appendChild(cellValue);
                    resultsTableBody.appendChild(row);
                }

                resultsContainer.classList.remove('ip-hidden');
            }
        } catch (error) {
            console.error("Error occurred while processing the image:", error);
            alert("An error occurred while processing the image. Please try again.");
        } finally {
            loadingIndicator.classList.add('ip-hidden');
        }
    });
});