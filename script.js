document.getElementById('timestepRange').addEventListener('input', (event) => {
    const timestep = event.target.value;
    updatePlot(timestep);
});

async function updatePlot(timestep) {
    try {
        const response = await fetch(`/plot?timestep=${timestep}`);
        if (response.ok) {
            const plotUrl = await response.json();
            document.getElementById('plotImage').src = plotUrl.url;
        } else {
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    } catch (error) {
        console.error('Error fetching plot:', error);
    }
}
