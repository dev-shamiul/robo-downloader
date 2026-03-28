// 🌙 Dark Mode Toggle
function toggleDarkMode() {
  document.body.classList.toggle("dark");
}

// Show Loader + Progress
function showLoader(event) {
  let box = document.querySelector(".box");
  let loader = box.querySelector(".loader");
  let progress = box.querySelector(".progress");
  let fill = box.querySelector(".progress-fill");
  let form = event.target;

  let input = form.querySelector("input[name='url']");
  if (!input.value.trim()) return false;

  let btn = form.querySelector("button");
  btn.disabled = true;

  // 🔥 Keep original text safe
  let originalText = btn.innerText;
  btn.setAttribute("data-text", originalText);
  btn.innerText = "Processing...";

  loader.classList.remove("hidden");
  progress.classList.remove("hidden");

  let width = 0;

  // 🔥 Clear previous interval if any
  if (window.progressInterval) {
    clearInterval(window.progressInterval);
  }

  window.progressInterval = setInterval(() => {
    if (width >= 95) {
      clearInterval(window.progressInterval);
    } else {
      width += 5;
      fill.style.width = width + "%";
    }
  }, 300);

  return true; // allow submit
}

// Reset after page reload (backend response)
window.addEventListener("load", () => {
  // hide loader
  document.querySelectorAll(".loader").forEach(l => l.classList.add("hidden"));

  // reset progress
  document.querySelectorAll(".progress").forEach(p => p.classList.add("hidden"));
  document.querySelectorAll(".progress-fill").forEach(f => f.style.width = "0%");

  // reset buttons safely
  document.querySelectorAll(".download-btn").forEach(btn => {
    btn.disabled = false;

    // 🔥 restore original text
    let originalText = btn.getAttribute("data-text");
    if (originalText) {
      btn.innerText = originalText;
    }
  });
});
