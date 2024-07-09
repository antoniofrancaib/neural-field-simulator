document.getElementById('uploadBtn').addEventListener('click', async () => {
    const nodesFile = document.getElementById('nodesFile').files[0];
    const elementsFile = document.getElementById('elementsFile').files[0];
    const synapticMatrixFile = document.getElementById('synapticMatrixFile').files[0];

    const formData = new FormData();
    formData.append('nodes', nodesFile);
    formData.append('elements', elementsFile);
    formData.append('synaptic_matrix', synapticMatrixFile);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert('Files uploaded successfully!');
            updatePlot(0); // Plot initial state after upload
        } else {
            alert('Error uploading files.');
        }
    } catch (error) {
        console.error('Error uploading files:', error);
    }
});

document.getElementById('timestepRange').addEventListener('input', (event) => {
    const timestep = event.target.value;
    updatePlot(timestep);
});

async function updatePlot(timestep) {
    try {
        const response = await fetch(`/plot?timestep=${timestep}`);
        const plotHtml = await response.text();
        document.getElementById('plotContainer').innerHTML = plotHtml;
    } catch (error) {
        console.error('Error fetching plot:', error);
    }
}
