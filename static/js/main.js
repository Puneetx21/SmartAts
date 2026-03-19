// Theme Toggle Functionality
document.addEventListener("DOMContentLoaded", () => {
  // ============ Theme Toggle ============
  const themeToggle = document.getElementById("themeToggle");
  const html = document.documentElement;
  
  // Get saved theme from localStorage; default to male theme
  const getSavedTheme = () => {
    const saved = localStorage.getItem("theme");
    if (saved === "male" || saved === "female") {
      return saved;
    }
    return "male";
  };
  
  const theme = getSavedTheme();
  html.setAttribute("data-theme", theme);
  
  // Toggle theme on button click
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const currentTheme = html.getAttribute("data-theme");
      const newTheme = currentTheme === "female" ? "male" : "female";
      html.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);
    });
  }
  
  // ============ Drop Zone & File Upload ============
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("resume");
  const fileName = document.getElementById("fileName");
  const uploadForm = document.getElementById("uploadForm");
  const loader = document.getElementById("loader");
  const submitBtn = document.getElementById("submitBtn");

  if (!dropZone || !fileInput) return;

  // Click to open file dialog
  dropZone.addEventListener("click", () => fileInput.click());

  // Drag over event
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add("drag-over");
  });

  // Drag leave event
  dropZone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove("drag-over");
  });

  // Drop event
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove("drag-over");
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      const fileNameLower = file.name.toLowerCase();
      const isValidType = fileNameLower.endsWith(".pdf") || fileNameLower.endsWith(".docx");
      
      // Validate file type
      if (!isValidType) {
        alert("❌ Please upload a PDF or DOCX file.");
        return;
      }
      
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert("❌ File size must be less than 10MB.");
        return;
      }
      
      fileInput.files = e.dataTransfer.files;
      displayFileName(file.name);
    }
  });

  // File input change event
  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) {
      displayFileName(fileInput.files[0].name);
    }
  });

  // Display file name
  function displayFileName(name) {
    fileName.textContent = "✅ Selected: " + name;
  }

  // Form submission
  if (uploadForm && submitBtn && loader) {
    uploadForm.addEventListener("submit", () => {
      submitBtn.disabled = true;
      loader.classList.remove("hidden");
    });
  }

  // ============ Smooth Scroll ============
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ============ Keyboard Shortcuts ============
  document.addEventListener('keydown', (e) => {
    // Alt + T = Toggle theme
    if (e.altKey && e.key === 't') {
      if (themeToggle) {
        themeToggle.click();
      }
    }
  });
});
