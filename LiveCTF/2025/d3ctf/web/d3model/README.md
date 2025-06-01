# D3MODEL

## Challenge Summary


The challenge exposes a Flask web application that allows uploading and validating Keras models via the `/upload` endpoint:

```
file.save(filepath)
keras.models.load_model(filepath)
``` 


The uploaded file is saved as test.keras and passed to `keras.models.load_model()` for validation. 
Only a JSON response indicating success or failure is returned.

### Vulnerability: CVE-2025-1550

I leverage `CVE-2025-1550`, a vulnerability that allows arbitrary code execution during Keras model deserialization.

Keras models saved in .keras format are ZIP archives containing a config.json file. 

This file defines the model structure as a JSON-based object graph. 
During deserialization, Keras reconstructs the model by:
- dynamically importing modules specified in the JSON,
- instantiating classes (or functions) using those module paths and names,
- and passing configuration parameters from the JSON directly into the constructor.


### Deserialization as Code Execution

If a malicious actor controls config.json, they can replace a legitimate layer with a payload like this:

- `"class_name": "function"`
- `"module": "subprocess"`
- `"config": "Popen"
` arguments and keyword arguments passed via `"inbound_nodes"`

This leads Keras to import subprocess, resolve Popen, and execute it with attacker-controlled arguments — **during model loading**.
No code is evaluated explicitly — the exploit abuses the **intended flexibility** of Keras' dynamic model deserialization, which lacks strict validation of module origins, class types, or function behavior.

### Exploitation Flow

- Upload a clean .keras model and modifying config.json
- Extract and modify `config.json` inside the archive:
  - Replace a layer definition with a malicious object:

```
{
  "class_name": "function",
  "module": "subprocess",
  "config": "Popen",
  "inbound_nodes": [{
    "args": [["sh", "-c", "<command>"]],
    "kwargs": {"bufsize": -1}
  }]
}
```

- Repackage the `.keras` file with the modified `config.json`.
- Upload the malicious model to trigger execution.



### Payload Example

To extract the flag from the container (in this case stored in an environment variable), I used:

```
"args": [["sh", "-c", "echo $FLAG > index.html"]]
```

Once the payload was uploaded, the Flask app served `index.html` directly at `/`, revealing the flag in the browser.

### Final Thoughts

This challenge highlights how poorly constrained deserialization mechanisms in machine learning frameworks can lead to remote code execution (RCE) — a severe security flaw, especially in automated ML pipelines or hosted model validators.
Once triggered, the exploit grants code execution with the same privileges as the server process — no need for uploads of scripts, binaries, or external tools.


### Reference

[https://blog.huntr.com/inside-cve-2025-1550-remote-code-execution-via-keras-models](https://blog.huntr.com/inside-cve-2025-1550-remote-code-execution-via-keras-models)


