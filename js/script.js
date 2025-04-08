document
.getElementById("generateMusicButton")
.addEventListener("click", () => {
  const video = document.getElementById("video");
  const emotionType = document.getElementById("emotionType");
  const audioPlayer = document.getElementById("audioPlayer");
  const songTitle = document.getElementById("songTitle");
  const songImage = document.getElementById("songImage");

  // Set video feed source
  video.src = "/video_feed";

  // Simulate emotion detection
  setTimeout(() => {
    fetch("/detect_emotion")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch emotion data");
        }
        return response.json();
      })
      .then((data) => {
        emotionType.textContent = data.emotion || "No emotion detected";

        if (data.song) {
          audioPlayer.src = data.song;
          songTitle.textContent = data.song.split("/").pop();
          audioPlayer.load();
          audioPlayer.play();
          togglePlayIcon(true);
        } else {
          console.warn("No song provided for the detected emotion.");
        }
      })
      .catch((error) => {
        console.error("Error fetching emotion data:", error);
      });
  }, 10000); // 10-second delay
});

// Music Player Controls
const audioPlayer = document.getElementById("audioPlayer");
const progressBar = document.querySelector(".progress-bar");
const progressHead = document.querySelector(".progress-head");
const currentTimeDisplay = document.querySelector(".current-time");
const durationDisplay = document.querySelector(".duration");
const playButton = document.querySelector(".play i");
const skipBackButton = document.getElementById("skipBackButton");
const skipForwardButton = document.getElementById("skipForwardButton");
const volumeSlider = document.getElementById("volumeSlider");

// Update progress bar as music plays
audioPlayer.addEventListener("timeupdate", () => {
if (audioPlayer.duration) {
  // Ensure duration is valid
  const progress =
    (audioPlayer.currentTime / audioPlayer.duration) * 100;
  progressBar.style.width = `${progress}%`;
  progressHead.style.left = `${progress}%`;

  const minutes = Math.floor(audioPlayer.currentTime / 60)
    .toString()
    .padStart(2, "0");
  const seconds = Math.floor(audioPlayer.currentTime % 60)
    .toString()
    .padStart(2, "0");
  currentTimeDisplay.textContent = `${minutes}:${seconds}`;
}
});

// Display total duration when loaded
audioPlayer.addEventListener("loadedmetadata", () => {
const minutes = Math.floor(audioPlayer.duration / 60)
  .toString()
  .padStart(2, "0");
const seconds = Math.floor(audioPlayer.duration % 60)
  .toString()
  .padStart(2, "0");
durationDisplay.textContent = `${minutes}:${seconds}`;
});

// Play/Pause Functionality
document.querySelector(".play").addEventListener("click", () => {
if (audioPlayer.paused) {
  audioPlayer.play();
  togglePlayIcon(true);
} else {
  audioPlayer.pause();
  togglePlayIcon(false);
}
});

// Skip Backward 10 Seconds
skipBackButton.addEventListener("click", () => {
audioPlayer.currentTime = Math.max(0, audioPlayer.currentTime - 10);
});

// Skip Forward 10 Seconds
skipForwardButton.addEventListener("click", () => {
audioPlayer.currentTime = Math.min(
  audioPlayer.duration,
  audioPlayer.currentTime + 10
);
});

// Volume control functionality


// Toggle Play/Pause Icon
function togglePlayIcon(isPlaying) {
if (isPlaying) {
  playButton.classList.replace("fa-play", "fa-pause");
} else {
  playButton.classList.replace("fa-pause", "fa-play");
}
}