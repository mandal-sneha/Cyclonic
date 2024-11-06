function displayCycloneMap() {
    const yearDropdown = document.getElementById("hc-year-dropdown");
    const selectedYear = yearDropdown.value;
    const cycloneMap = document.getElementById("hc-cyclone-map");
    const cycloneSections = document.querySelectorAll(".hc-cyclone-item");

    // Update the image source based on the selected year
    cycloneMap.src = `/static/${selectedYear}_cyclones.png`;
    cycloneMap.alt = `Cyclone paths for ${selectedYear}`;

    // Display the image
    cycloneMap.style.display = "block";

    // Show or hide cyclone sections based on selected year
    cycloneSections.forEach(section => {
        section.style.display = section.id === `cyclone-${selectedYear}` ? "block" : "none";
    });
}

function toggleDescription(descriptionId) {
    const description = document.getElementById(descriptionId);
    const cycloneName = description.previousElementSibling;

    if (description.style.display === "block") {
        description.style.display = "none";
        cycloneName.classList.remove("open");
    } else {
        description.style.display = "block";
        cycloneName.classList.add("open");
    }
}