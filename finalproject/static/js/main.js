let counter;

// Timer
function startTimer() {

  //Get start-timer buttons
  let buttons = document.getElementsByClassName("start-timer");
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].setAttribute("disabled", "true");
  }

  // Select timeout Audio element
  const timeoutAudio = document.getElementById("timeout_audio");

  // Initialize timeout sound
  timeoutAudio.src = "http://soundbible.com/grab.php?id=2218&type=mp3";
  timeoutAudio.load();

  let count = 0;
  counter = setInterval(function () {
    count--;

    let minutes = Math.floor(count / 60);
    let seconds = count % 60;
    document.getElementById("timer").innerHTML = `${minutes}:${
      seconds < 10 ? "0" + seconds : seconds
    }`;

    // If timer hits zero
    if (count <= 0) 
    {  
        clearInterval(counter);
        timeoutAudio.play();
        document.getElementById("timer").innerHTML = "";

      // Disable all buttons while timer is running
      for (let i = 0; i < buttons.length; i++) {
        buttons[i].removeAttribute("disabled");
      }
    }
  }, 1000);
}


function stopTimer() {

    //clear the Timer and timerId in the page
    clearInterval(counter);
    document.getElementById("timer").innerHTML = "";

    // Enable start-timer buttons again
    let buttons = document.getElementsByClassName("start-timer");

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].removeAttribute("disabled");
    }
}


function swapIcon(id) {

    // Replace the start-timer button with an stop-timer
    let button = document.getElementById(id);
    let stopTimer = document.getElementById(id.replace("start-timer", "stop-timer"));
    
    button.style.display = "none";
    stopTimer.style.display = "inline";

    // Disable input
    let input1 = button.closest('tr').getElementsByTagName("input")[0];
    input1.setAttribute("disabled", true);

    let input2 = button.closest('tr').getElementsByTagName("input")[1];
    input2.setAttribute("disabled", true);

    // When the X for stop-timer gets clicked
    stopTimer.addEventListener("click", function() 
    {
        stopTimer.style.display = "none";
        button.style.display = "inline";

        // Re-enable input
        input1.removeAttribute("disabled");
        input2.removeAttribute("disabled");
        
    });
}

// Search function jQuery bootstrap
$(document).ready(function() {
    // Listen for changes to the search input
    $('#search-input').on('input', function() {
        const searchQuery = $(this).val().toLowerCase();
        // Hide or show program cards based on the search query
        $('#cards-container .card').each(function() {
            const programName = $(this).find('.card-title').text().toLowerCase();
            const programDescription = $(this).find('.card-text').text().toLowerCase();
            if (programName.includes(searchQuery) || programDescription.includes(searchQuery)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });  
});

// function to calculate one rep max based on weight and reps
$(document).ready(function() {
    const weightInput = $('#weight-input');
    const repsInput = $('#reps-input');
    const oneRepMaxInput = $('#one-rep-max-input');

    const calculateMax = () => {
        const weight = weightInput.val();
        const reps = repsInput.val();
        const oneRepMax = weight * (1 + reps/30);

        oneRepMaxInput.val(oneRepMax.toFixed(1));
        };

    weightInput.on('input', calculateMax);
    repsInput.on('input', calculateMax);
});


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
  