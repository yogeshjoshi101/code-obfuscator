function displayOutput(result) {
  document.getElementById("output").value = result;
}

function displaySecurityKey(key) {
  alert("Security Key: " + key);
}

function obfuscateCode() {
  const code = document.getElementById("codeInput").value;
  fetchObfuscate(code);
}

function deobfuscateCode() {
  const code = document.getElementById("output").value;
  const securityKey = document.getElementById("securityKey").value;
  fetchDeobfuscate(code, securityKey);
}
