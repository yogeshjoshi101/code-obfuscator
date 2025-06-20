async function fetchObfuscate(code, features = null) {
  try {
    const response = await fetch("http://127.0.0.1:5000/obfuscate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(features ? { code, features } : { code })
    });
    const data = await response.json();
    displayOutput(data.obfuscated_code);
  } catch (error) {
    console.error("Error during obfuscation:", error);
  }
}

async function fetchDeobfuscate(code) {
  try {
    const response = await fetch("http://127.0.0.1:5000/deobfuscate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: code })
    });
    const data = await response.json();
    displayOutput(data.deobfuscated_code);
  } catch (error) {
    console.error("Error during deobfuscation:", error);
  }
}
