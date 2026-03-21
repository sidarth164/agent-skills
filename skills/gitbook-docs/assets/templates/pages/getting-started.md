---
description: "Get {{ project_name }} running locally in under 5 minutes"
---

# Quick Start

{% hint style="info" %}
This guide gets you from clone to running as fast as possible.
See [Prerequisites](prerequisites.md) for system requirements and
[Development Setup](development-setup.md) for the full environment setup.
{% endhint %}

{% stepper %}
{% step %}
## Clone the repository

```bash
git clone {{ repo_url }}
cd {{ project_dir }}
```
{% endstep %}

{% step %}
## Install dependencies

{{ Language-specific: cargo build, pip install, npm install, etc. }}
{% endstep %}

{% step %}
## Configure

{{ Minimal configuration needed — env vars, config files, credentials. }}
{% endstep %}

{% step %}
## Run

{{ The command to start the project — cargo run, python main.py, npm start, etc. }}
{% endstep %}

{% step %}
## Verify

{{ How to confirm it's working — curl an endpoint, run a smoke test, check logs. }}
{% endstep %}
{% endstepper %}
