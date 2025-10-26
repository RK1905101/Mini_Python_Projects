document.getElementById("askBtn").addEventListener("click", async () => {
  const question = document.getElementById("question").value.trim();
  const answerBox = document.getElementById("answer");
  const loadingEl = document.getElementById("loading");

  answerBox.textContent = "";
  loadingEl.style.display = "block";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const urlParams = new URLSearchParams(new URL(tab.url).search);
  const videoId = urlParams.get("v");

  if (!videoId) {
    loadingEl.style.display = "none";
    answerBox.textContent = "Not a valid YouTube video.";
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: videoId, question })
    });

    const data = await response.json();
    answerBox.textContent = response.ok ? data.answer : "Error: " + data.detail;
  } catch (err) {
    answerBox.textContent = "Failed to connect to backend.";
  }

  loadingEl.style.display = "none";
});
