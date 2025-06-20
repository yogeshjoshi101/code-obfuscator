function isLikelyObfString(str) {
  // crude check: long, only base64 chars, and decodes to JSON
  if (!str || str.length < 20) return false;
  try {
    const decoded = atob(str);
    JSON.parse(decoded);
    return true;
  } catch {
    return false;
  }
}

function displayOutput(result, obfString = null) {
  document.getElementById("output").value = result || "";
  if (obfString !== null) {
    document.getElementById("deobfString").value = obfString;
    lastObfuscationString = obfString;
  }
  showToast("Done!", "success");
}

function getObfKey() {
  return document.getElementById("obfKey").value.trim();
}
function getDeobfKey() {
  return document.getElementById("deobfKey").value.trim();
}

// Patch fetchObfuscate to send key
async function fetchObfuscate(code, features = null, key = "") {
  try {
    const response = await fetch("http://127.0.0.1:5000/obfuscate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(features ? { code, features, key } : { code, key })
    });
    const data = await response.json();
    if (data.obfuscated_code) {
      // Show the base64 string in the deobfString field
      document.getElementById("deobfString").value = data.obfuscated_code;
      lastObfuscationString = data.obfuscated_code;
      // Show the actual obfuscated code in the output textarea (decode it)
      const decoded = atob(data.obfuscated_code);
      const payload = JSON.parse(decoded);
      document.getElementById("output").value = payload.code || "";
      showToast("Obfuscation complete!", "success");
    } else {
      displayOutput("", "");
      showToast(data.error || "Obfuscation failed", "error");
    }
  } catch (error) {
    displayOutput("", "");
    showToast("Error during obfuscation", "error");
  }
}

// Patch fetchDeobfuscate to send key
async function fetchDeobfuscate(obfString, key) {
  try {
    const response = await fetch("http://127.0.0.1:5000/deobfuscate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: obfString, key })
    });
    const data = await response.json();
    if (data.deobfuscated_code !== undefined) {
      document.getElementById("output").value = data.deobfuscated_code || "";
      showToast("Deobfuscation complete!", "success");
    } else {
      showToast(data.error || "Deobfuscation failed", "error");
    }
  } catch (error) {
    showToast("Error during deobfuscation", "error");
  }
}

// Add event for copy button
document.getElementById("copyDeobfBtn").onclick = function() {
  const str = document.getElementById("deobfString").value;
  if (str) {
    navigator.clipboard.writeText(str);
    showToast("Deobfuscation string copied!", "success");
  } else {
    showToast("Nothing to copy!", "error");
  }
};

// Allow user to paste a base64 string and deobfuscate it
document.getElementById("deobfString").addEventListener("input", function(e) {
  const val = e.target.value.trim();
  if (val.length > 20) { // crude check for base64
    fetchDeobfuscate(val);
  }
});

function obfuscateCode() {
  const code = document.getElementById("codeInput").value;
  const key = getObfKey();
  if (!code.trim()) {
    showToast("Input code is empty!", "error");
    return;
  }
  if (!key) {
    showToast("Please enter a key for obfuscation!", "error");
    return;
  }
  fetchObfuscate(code, null, key);
}

function deobfuscateCode() {
  const deobfString = document.getElementById("deobfString").value.trim();
  const key = getDeobfKey();
  if (!deobfString) {
    showToast("Paste the deobfuscation string!", "error");
    return;
  }
  if (!key) {
    showToast("Please enter the key used for obfuscation!", "error");
    return;
  }
  fetchDeobfuscate(deobfString, key);
}

// File upload logic
document.getElementById("fileInput").addEventListener("change", async function(e) {
  const file = e.target.files[0];
  if (file && file.name.endsWith(".py")) {
    await handleFileUpload(file);
  } else {
    showToast("Please upload a .py file", "error");
  }
});

// Drag-and-drop upload
const uploadZone = document.getElementById("uploadZone");
const fileInput = document.getElementById("fileInput");
const filePreview = document.getElementById("filePreview");
const uploadText = document.getElementById("uploadText");

if (uploadZone) {
  uploadZone.addEventListener("dragover", e => {
    e.preventDefault();
    uploadZone.classList.add("dragover");
  });
  uploadZone.addEventListener("dragleave", e => {
    e.preventDefault();
    uploadZone.classList.remove("dragover");
  });
  uploadZone.addEventListener("drop", async e => {
    e.preventDefault();
    uploadZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith(".py")) {
      await handleFileUpload(file);
    } else {
      showToast("Please upload a .py file", "error");
    }
  });
  uploadZone.addEventListener("click", () => fileInput.click());
}

async function handleFileUpload(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch("http://127.0.0.1:5000/upload", {
    method: "POST",
    body: formData
  });
  const data = await res.json();
  if (data.code) {
    document.getElementById("codeInput").value = data.code;
    filePreview.textContent = file.name;
    filePreview.classList.add("active");
    showToast("File loaded!", "success");
  } else if (data.error) {
    showToast(data.error, "error");
  }
}

// Download logic
document.getElementById("downloadBtn").addEventListener("click", async function() {
  const code = document.getElementById("output").value;
  if (!code.trim()) {
    showToast("Nothing to download!", "error");
    return;
  }
  const filename = "output.py";
  const res = await fetch("http://127.0.0.1:5000/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, filename })
  });
  if (res.ok) {
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    showToast("Download started!", "success");
  } else {
    showToast("Download failed!", "error");
  }
});

// Clear editors
function clearEditors() {
  document.getElementById("codeInput").value = "";
  document.getElementById("output").value = "";
  filePreview.textContent = "";
  filePreview.classList.remove("active");
  showToast("Cleared!", "success");
}

// Button actions
document.getElementById("obfuscateBtn").onclick = obfuscateCode;
document.getElementById("deobfuscateBtn").onclick = deobfuscateCode;
document.getElementById("clearBtn").onclick = clearEditors;
document.getElementById("downloadBtn").onclick = downloadOutput;
document.getElementById("toggleEditBtn").onclick = toggleOutputEdit;

// Toast notification system
function showToast(message, type = "info") {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = "toast show";
  if (type === "error") toast.style.background = "#ff416c";
  else if (type === "success") toast.style.background = "#4f8cff";
  else toast.style.background = "rgba(255,255,255,0.92)";
  setTimeout(() => {
    toast.className = "toast";
    toast.style.background = "";
  }, 2600);
}

// Output read-only toggle
function toggleOutputEdit() {
  const output = document.getElementById("output");
  const icon = document.getElementById("toggleEditIcon");
  if (output.hasAttribute("readonly")) {
    output.removeAttribute("readonly");
    output.classList.add("editable");
    icon.textContent = "✏️";
    showToast("Output is now editable");
  } else {
    output.setAttribute("readonly", "readonly");
    output.classList.remove("editable");
    icon.textContent = "🔒";
    showToast("Output is now read-only");
  }
}
