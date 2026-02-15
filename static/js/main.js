document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("resume");
  const fileName = document.getElementById("fileName");
  const uploadForm = document.getElementById("uploadForm");
  const loader = document.getElementById("loader");
  const submitBtn = document.getElementById("submitBtn");

  if (!dropZone || !fileInput || !uploadForm) return;

  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
  });

  dropZone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (!file.name.toLowerCase().endsWith(".pdf")) {
        alert("Please upload a PDF file.");
        return;
      }
      fileInput.files = e.dataTransfer.files;
      fileName.textContent = file.name;
    }
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) {
      fileName.textContent = fileInput.files[0].name;
    }
  });

  uploadForm.addEventListener("submit", () => {
    submitBtn.disabled = true;
    loader.classList.remove("hidden");
  });
});
