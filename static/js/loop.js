document.addEventListener("DOMContentLoaded", function () {
    const audioPlayers = document.querySelectorAll("audio");
    const loopButton = document.getElementById("loopButton");

    if (!audioPlayers.length) {
        console.warn("Brak odtwarzaczy audio!");
        return;
    }

    let isLooping = false;

    loopButton.addEventListener("click", function () {
        isLooping = !isLooping;
        audioPlayers.forEach(audio => {
            audio.loop = isLooping;
        });
        loopButton.textContent = isLooping ? "🔁 Zapętlanie: WŁ." : "🔁 Zapętlanie: WYŁ.";
    });


    audioPlayers.forEach(audio => {
        audio.addEventListener("ended", function () {
            console.log("Utwór zakończony. Loop: " + audio.loop);
        });
    });
});
