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

  let count = 5;
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

     // Disable input fields for the row that the clicked start button belongs to
    let row = button.closest('tr');
    let inputs = row.getElementsByTagName('input');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].disabled = true;
    }

    // When the X for stop-timer gets clicked
    stopTimer.addEventListener("click", function() 
    {
        event.preventDefault(); // prevent form submission behavior
        stopTimer.style.display = "none";
        button.style.display = "inline";

        // Re-enable input
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].disabled = false;
        }
        
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


// Automaticallu close or fade away bootstrap flash messages
$(document).ready(function () {
 
    window.setTimeout(function() {
        $(".alert").fadeTo(1000, 0).slideUp(1000, function(){
            $(this).remove(); 
        });
    }, 2500);
     
    });
