async function fetchObfuscate(code) {
  try {
    const response = await fetch("http://127.0.0.1:5000/obfuscate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: code })
    });
    const data = await response.json();
    displayObfuscatedOutput(data.obfuscated_code);
    displayOutput(data.obfuscated_encoded_code);
    displaySecurityKey(data.security_key);
  } catch (error) {
    console.error("Error during obfuscation:", error);
  }
}

async function fetchDeobfuscate(code, securityKey) {
  try {
    const response = await fetch("http://127.0.0.1:5000/deobfuscate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: code, security_key: securityKey })
    });
    const data = await response.json();
    displayOutput(data.deobfuscated_code);
  } catch (error) {
    console.error("Error during deobfuscation:", error);
  }
}
