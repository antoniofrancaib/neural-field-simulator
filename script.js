document.getElementById('startBtn').addEventListener('click', function() {
    const connectivity = document.getElementById('connectivity').value;
    fetch('http://localhost:5000/simulate', {  // Ensure the URL matches your Flask server URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ connectivity: connectivity })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Simulation results:', data);
        plotResults(data.time, data.activities);
    })
    .catch(error => console.error('Error:', error));
});

function plotResults(time, activities) {
    var data = [{
        z: activities,
        type: 'surface'
    }];

    var layout = {
        title: 'Neural Field Simulation',
        autosize: false,
        width: 500,
        height: 500,
        margin: {
            l: 65,
            r: 50,
            b: 65,
            t: 90,
        }
    };

    Plotly.newPlot('plot', data, layout);
}
