document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('pp-predictor-form');
    const loadingIndicator = document.getElementById('pp-loading-indicator');
    const cycloneMap = document.getElementById('pp-cyclone-map');
    let loadingAnimation;

    const startLoadingAnimation = () => {
        loadingIndicator.classList.remove('pp-hidden');
        let rotation = 0;
        loadingAnimation = setInterval(() => {
            rotation += 2;
            const spinner = loadingIndicator.querySelector('.pp-spinner');
            spinner.style.transform = `rotate(${rotation}deg)`;
        }, 10);
    };

    const stopLoadingAnimation = () => {
        if (loadingAnimation) {
            clearInterval(loadingAnimation);
        }
        loadingIndicator.classList.add('pp-hidden');
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        cycloneMap.style.display = 'none';
        startLoadingAnimation();

        const formData = new FormData(form);
        const params = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            params.append(key, value);
        }

        try {
            const response = await fetch(`/generate_map?${params.toString()}`);
            const data = await response.json();

            if (data.success) {
                cycloneMap.src = `${data.image_url}?t=${new Date().getTime()}`;
            } else {
                alert('Error generating map: ' + data.error);
                stopLoadingAnimation();
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating the map');
            stopLoadingAnimation();
        }
    });

    cycloneMap.addEventListener('load', () => {
        stopLoadingAnimation();
        cycloneMap.style.display = 'block';
    });
});