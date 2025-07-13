// document.getElementById("summarize").addEventListener("click", async () => {
//   const url = document.getElementById("url").value;
//   const resultDiv = document.getElementById("result");
//   resultDiv.innerText = "Summarizing...";

//   try {
//     const response = await fetch("http://localhost:5000/summarize", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ url: url }),
//     });

//     const data = await response.json();
//     resultDiv.innerText = data.summary || ("Error: " + data.error);
//   } catch (err) {
//     resultDiv.innerText = "Failed to connect to backend.";
//   }
// });
window.addEventListener("DOMContentLoaded", () => {
  const urlInput = document.getElementById("url");
  const resultDiv = document.getElementById("result");
  const summarizeBtn = document.getElementById("summarize");

  // Auto-detect YouTube tab
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    if (tab && tab.url && tab.url.includes("youtube.com/watch")) {
      urlInput.value = tab.url;  // Autofill the input
    }
  });

  summarizeBtn.addEventListener("click", async () => {
    const url = urlInput.value;
    resultDiv.innerText = "Summarizing...";

    try {
      const response = await fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url }),
      });

      const data = await response.json();
      resultDiv.innerText = data.summary || ("Error: " + data.error);
    } catch (err) {
      resultDiv.innerText = "Failed to connect to backend.";
    }
  });
});

