if (window.location.href.indexOf('/statistics') !== -1) {
    // Initialize chart.js stuff
    var ctx = document.getElementById("myChart").getContext("2d");
    var myChart = new Chart(ctx, {
        type: "line",
        data: {
        labels: [], // initialize labels array
        datasets: [], // initialize datasets array
        },
    });

    // Define colors for each exercise
    const benchPressColor = 'rgba(187, 134, 252, 0.6)';
    const squatColor = 'rgba(51, 225, 237, 0.6)';
    const deadliftColor = 'rgba(3, 218, 197, 0.6)';
    const overheadPressColor = 'rgba(207, 102, 121, 0.6)';
    const barbellRowColor = 'rgba(155, 155, 20, 0.6)';

    fetch('/data')
        .then(response => response.json())
        .then(data => {
            for (const [exercise, sets] of Object.entries(data)) {
                // extract labels and data for each exercise
                const labels = sets.map(set => set.date);
                const data = sets.map(set => set.onerm);

                // set color for each exercise
                let backgroundColor;
                switch (exercise) {
                    case 'Bench Press (Barbell)':
                        backgroundColor = benchPressColor;
                        break;
                    case 'Squat (Barbell)':
                        backgroundColor = squatColor;
                        break;
                    case 'Deadlift (Barbell)':
                        backgroundColor = deadliftColor;
                        break;
                    case 'Overhead Press (Barbell)':
                        backgroundColor = overheadPressColor;
                        break;
                    case 'Barbell Row':
                        backgroundColor = barbellRowColor;
                        break;
                    default:
                        backgroundColor = 'rgba(0, 0, 0, 0)';
                        break;
                }
            
                // add dataset to chart data
                myChart.data.datasets.push({
                    label: exercise,
                    data: data,
                    backgroundColor: backgroundColor
                });


                // add labels to chart data
                if (myChart.data.labels.length == 0) {
                    myChart.data.labels = labels;
                }
            }

            // update chart with new data
            myChart.update();
        });
}