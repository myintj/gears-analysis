// script.js

// Optionally add some client-side checks, e.g., verifying file type or size before uploading
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file");
    if (fileInput) {
      fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file && file.type !== "text/csv") {
          alert("Please upload a valid CSV file.");
          e.target.value = ""; // reset
        }
      });
    }
  });
  