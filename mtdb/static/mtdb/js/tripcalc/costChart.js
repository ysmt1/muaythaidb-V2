const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        datasets: [{
            data: [0, 0, 0, 0, 0, 0, 0],
            backgroundColor: ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628"]
            // alternate lighter colors: ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494"]
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Training',
            'Accomodation',
            'Food',
            'Transportation',
            'Entertainment',
            'Misc',
            'Travel'
        ]
    },
    options: {
        title: {
            display: true,
            text: 'Cost Breakdown (฿)',
            fontSize: 16
        },
    }
});

function updateChart(data) {
    myChart.data.datasets[0].data = data;
    myChart.update();
}