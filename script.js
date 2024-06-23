async function simulate() {
    const timestep = document.getElementById('timestep').value;
    const response = await fetch(`/simulate?timestep=${timestep}`);
    const data = await response.json();
    const image = document.getElementById('simulationImage');
    image.src = 'data:image/png;base64,' + data.image;
}
