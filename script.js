document.addEventListener("DOMContentLoaded", function() {
    const simulateButton = document.getElementById('simulate');
    const resetButton = document.getElementById('reset');
    const firingThresholdSlider = document.getElementById('firing-threshold');
    const adaptivitySlider = document.getElementById('adaptivity');
    const simulationImage = document.getElementById('simulationImage');
    const colorMapRadios = document.getElementsByName('colormap');

    function getSelectedColorMap() {
        for (let radio of colorMapRadios) {
            if (radio.checked) {
                return radio.value;
            }
        }
    }

    function updateSimulation() {
        const timestep = 0; // Set this value based on your logic
        const firingThreshold = firingThresholdSlider.value;
        const adaptivity = adaptivitySlider.value;
        const colorMap = getSelectedColorMap();

        fetch(`https://your-heroku-app.herokuapp.com/simulate?timestep=${timestep}&firing_threshold=${firingThreshold}&adaptivity=${adaptivity}&colormap=${colorMap}`)
            .then(response => response.json())
            .then(data => {
                simulationImage.src = 'data:image/png;base64,' + data.image;
            });
    }

    simulateButton.addEventListener('click', updateSimulation);
    resetButton.addEventListener('click', function() {
        firingThresholdSlider.value = 5;
        adaptivitySlider.value = 5;
        updateSimulation();
    });

    // Presets buttons logic
    document.getElementById('localized-spots').addEventListener('click', function() {
        // Your logic to apply localized spots preset
        updateSimulation();
    });
    document.getElementById('traveling-waves').addEventListener('click', function() {
        // Your logic to apply traveling waves preset
        updateSimulation();
    });
    // Add similar event listeners for other preset buttons

    // Initialize the simulation on page load
    updateSimulation();
});
