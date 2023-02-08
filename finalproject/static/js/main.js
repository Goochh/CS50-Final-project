
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

  let count = 10;
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

