// Timer
function startTimer() {
  //Get all buttons
  let buttons = document.getElementsByClassName("material-symbols-outlined");
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].setAttribute("disabled", "true");
  }

  // Select timeout Audio element
  const timeoutAudio = document.getElementById("timeout_audio");

  // Initialize timeout sound
  timeoutAudio.src = "http://soundbible.com/grab.php?id=2218&type=mp3";
  timeoutAudio.load();

  let count = 120;
  let counter = setInterval(function () {
    count--;

    let minutes = Math.floor(count / 60);
    let seconds = count % 60;
    document.getElementById("timer").innerHTML = `${minutes}:${
      seconds < 10 ? "0" + seconds : seconds
    }`;

    if (count <= 0) {
      // If timer hits zero
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
