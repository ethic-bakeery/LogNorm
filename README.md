# LogNorm

> **"jq for Security Logs"**  Convert raw Linux logs into structured, normalized output from a single command.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP-orange.svg)]()
[![Domain](https://img.shields.io/badge/Domain-Cybersecurity-red.svg)]()

---

## What Is LogNorm?

LogNorm is a lightweight, stateless CLI tool built for **SOC analysts**, **security engineers**, and **cybersecurity students** who need fast, structured insight from raw Linux logs without writing complex regex, awk, grep, or sed commands.

Instead of this:

```bash
grep "Failed password" /var/log/auth.log | awk '{print $11, $13}' | sort | uniq -c | sort -rn
```

You run this:

```bash
lognorm analyze /var/log/auth.log --suspicious-only
```

And immediately get structured, color-coded, analyst-ready output.

---

## The Problem

When analyzing logs manually, analysts must:

- Know awk, grep, sed, and each log format deeply
- Write fragile regex that breaks across log format variations
- Mentally parse timestamps, PIDs, and hostnames on every line
- Rebuild the same one-liners repeatedly across incidents

Even experienced analysts struggle when switching between log types, handling inconsistent formats, or training junior team members under time pressure.

**LogNorm removes that complexity layer entirely.**

---

## Key Features

- **Auto-detection** LogNorm identifies the log type automatically. No `--type` flag required.
- **Normalized schema** Every log, regardless of source, maps to the same consistent field names.
- **Suspicious event detection** Brute-force attempts, root logins, and privilege escalation are flagged automatically with plain-English reasons.
- **Multiple output formats** Rich terminal table, JSON Lines, and CSV pipe-friendly by design.
- **Streaming** Handles large files without loading them fully into memory.
- **Filter and search** Filter by severity, user, IP, time range, or suspicious flag without post-processing.
- **Student-friendly** `lognorm explain` describes any log line in plain English.
- **No infrastructure** No daemon, no database, no config file required to get started.

---

## Installation

### From PyPI (recommended)

```bash
pip install lognorm
```

### From Source

```bash
git clone https://github.com/YOURUSERNAME/lognorm.git
cd lognorm
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Verify Installation

```bash
lognorm --version
lognorm --help
```

---

## Quick Start

### Analyze a log file

```bash
lognorm analyze /var/log/auth.log
```

### Read from stdin

```bash
cat /var/log/auth.log | lognorm analyze --stdin
tail -f /var/log/auth.log | lognorm analyze --stdin
```

### Show only suspicious events

```bash
lognorm analyze /var/log/auth.log --suspicious-only
```

### Export to JSON Lines

```bash
lognorm analyze /var/log/auth.log --format jsonl > events.jsonl
```

### Export to CSV

```bash
lognorm analyze /var/log/auth.log --format csv > events.csv
```

### Get a summary report

```bash
lognorm analyze /var/log/auth.log --summary
```

### Detect log type

```bash
lognorm detect /var/log/auth.log
# Output: auth.log: Linux Auth Log (confidence: 97%)
```

### See annotated sample lines

```bash
lognorm sample /var/log/auth.log
```

### Explain a specific line

```bash
lognorm explain /var/log/auth.log --line 42
```

---

## Commands

### `lognorm analyze <file> [options]`

Parse, normalize, and display log events.

| Flag | Description | Default |
|---|---|---|
| `--stdin` | Read from stdin instead of file | False |
| `--format` | Output format: `table`, `jsonl`, `csv` | `table` |
| `--severity` | Filter by severity eg `HIGH,CRITICAL` | All |
| `--user` | Filter by username | All |
| `--ip` | Filter by IP address | All |
| `--after` | Show events after timestamp (ISO 8601) | None |
| `--before` | Show events before timestamp (ISO 8601) | None |
| `--suspicious-only` | Show only flagged suspicious events | False |
| `--summary` | Show summary report instead of event table | False |
| `--no-color` | Disable ANSI color output | False |

### `lognorm detect <file>`

Identify the log type with a confidence score.

### `lognorm sample <file>`

Display 10 representative lines with parsed field annotations. Useful for understanding what LogNorm extracts before running a full analysis.

### `lognorm explain <file> --line <N>`

Display line N with a plain-English explanation of the event, extracted fields, and the reason for any suspicious flags.

---

## Output Schema

Every log event regardless of source is normalized to the same schema:

```json
{
  "event_id": "a3f2c1d4-...",
  "timestamp": "2024-02-28T10:42:11+00:00",
  "host": "prod-server-01",
  "log_type": "auth",
  "severity": "HIGH",
  "message": "Failed password for root from 192.168.1.100 port 52341 ssh2",
  "raw": "Feb 28 10:42:11 prod-server-01 sshd[3821]: Failed password for root from 192.168.1.100 port 52341 ssh2",
  "user": "root",
  "ip_address": "192.168.1.100",
  "port": 52341,
  "process_name": "sshd",
  "process_id": 3821,
  "auth_result": "failure",
  "auth_method": "password",
  "is_suspicious": true,
  "detection_reason": "Failed login attempt targeting root account",
  "tags": ["failed_login", "root_target"],
  "schema_version": "1.0.0",
  "source_file": "/var/log/auth.log"
}
```

### Severity Levels

| Severity | Color | Meaning |
|---|---|---|
| CRITICAL | 🔴 Red | Immediate threat indicator |
| HIGH | 🟠 Orange | Strong suspicious signal |
| MEDIUM | 🟡 Yellow | Warrants investigation |
| LOW | ⚪ White | Minor anomaly |
| INFO | Grey | Normal operational event |

---

## Supported Log Types

| Log Type | Format | Status |
|---|---|---|
| Linux Auth Log | `/var/log/auth.log` | ✅ Supported |
| Syslog | `/var/log/syslog` (RFC 3164/5424) | ✅ Supported |
| SSH Authentication | sshd entries in auth.log | ✅ Supported |
| Apache Access Log | Combined Log Format | 🔜 Coming Soon |
| Nginx Access Log | Default format | 🔜 Coming Soon |
| journald | `journalctl` output | 🔜 Coming Soon |
| Windows Event Log | Exported XML/CSV | 🔜 Planned |
| Auditd | `/var/log/audit/audit.log` | 🔜 Planned |

---

## Detection Rules

LogNorm includes built-in detection rules that flag suspicious patterns automatically:

| Rule | Trigger | Severity |
|---|---|---|
| Brute Force | 5+ failed logins from same IP within 60s | CRITICAL |
| Successful Login After Failures | Login success after 3+ prior failures from same IP | HIGH |
| Root Login Attempt | Any authentication attempt for root account | HIGH |
| Privilege Escalation | sudo usage or su to root | HIGH |
| New Source IP | Login from IP not seen previously in the session | MEDIUM |
| Off-Hours Login | Successful login outside 08:00–18:00 | MEDIUM |

Every flagged event includes a `detection_reason` field with a plain-English explanation.

---

## Integration Examples

### Pipe into Python / Pandas

```bash
lognorm analyze /var/log/auth.log --format jsonl | python3 analyze.py
```

```python
import sys, json, pandas as pd

events = [json.loads(line) for line in sys.stdin]
df = pd.DataFrame(events)
print(df[df['is_suspicious']].groupby('ip_address').size())
```

### Pipe into DuckDB

```bash
lognorm analyze /var/log/auth.log --format jsonl | \
  duckdb -c "SELECT ip_address, COUNT(*) as attempts FROM read_json('/dev/stdin') WHERE auth_result='failure' GROUP BY 1 ORDER BY 2 DESC"
```

### Pipe into jq

```bash
lognorm analyze /var/log/auth.log --format jsonl | \
  jq 'select(.is_suspicious == true) | {user, ip_address, detection_reason}'
```

### Remote analysis over SSH

```bash
ssh user@remote-server "cat /var/log/auth.log" | lognorm analyze --stdin --suspicious-only
```

### Save and review later

```bash
lognorm analyze /var/log/auth.log --format jsonl > /tmp/incident-$(date +%Y%m%d).jsonl
```

---

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | File not found or unreadable |
| 2 | Log type could not be detected |
| 3 | All lines failed to parse |
| 4 | Invalid arguments |

These are stable and safe to rely on in scripts and pipelines.

---

## Architecture

LogNorm is designed around a simple, linear data pipeline:

```
Raw Log File / stdin
        │
        ▼
    [ Reader ]          — Streams lines, handles file/stdin/encoding
        │
        ▼
   [ Detector ]         — Identifies log type with confidence score
        │
        ▼
    [ Parser ]          — Extracts fields via deterministic regex
        │
        ▼
  [ Normalizer ]        — Maps to NormalizedEvent schema (Pydantic)
        │
        ▼
  [ Detections ]        — Applies suspicious event rules
        │
        ▼
  [ Formatter ]         — Renders table / JSON Lines / CSV
        │
        ▼
      Output
```

Each stage is independent and replaceable. Adding a new log type means writing one new parser class. Adding a new output format means writing one new formatter class.

---

## Adding a Custom Parser (Plugin System)

Drop a Python file into `~/.lognorm/parsers/`. LogNorm discovers and loads it automatically.

Your parser must implement two methods:

```python
from lognorm.schema.normalized_event import NormalizedEvent

class MyCustomParser:
    
    def detect(self, line: str) -> float:
        """
        Return a confidence score between 0.0 and 1.0.
        1.0 = definitely this format. 0.0 = definitely not.
        """
        if "MY_APP" in line:
            return 0.95
        return 0.0

    def parse(self, line: str) -> NormalizedEvent:
        """
        Parse a single log line and return a NormalizedEvent.
        """
        # your parsing logic here
        return NormalizedEvent(
            event_id=...,
            raw=line,
            ...
        )
```

That's the entire interface. LogNorm validates your parser on load and reports any errors clearly.

---

## Design Philosophy

**1. Deterministic parsing first.** LogNorm never guesses. Every field in the output came from a specific, traceable regex match. You can always verify why a field has a particular value.

**2. AI as enhancement, not replacement.** The core tool works fully offline, with no API calls. AI-assisted features (unknown format detection, plain-English summaries) are opt-in additions, not requirements.

**3. No infrastructure by default.** No daemon. No database. No config file required. Install and run in under two minutes.

**4. Pipe friendly output.** LogNorm is designed to be one step in a pipeline, not a destination. Clean JSON Lines output integrates with jq, DuckDB, Pandas, Splunk, Elastic, and anything else you already use.

**5. Analyst ergonomics first.** Every design decision is tested against one scenario: a tired analyst at 2am on an unfamiliar system during an incident. Speed-to-insight over completeness.

---

## Roadmap

### v1.0 MVP (Current)
- [x] Auth.log, syslog, SSH parsing
- [x] Normalized schema v1
- [x] Rich table, JSON Lines, CSV output
- [x] Brute force, root login, privilege escalation detection
- [x] Filtering by severity, user, IP, time range
- [x] Summary report
- [x] Plugin system for custom parsers

### v1.1 Enrichment
- [ ] Apache and Nginx access log parsers
- [ ] GeoIP lookup (`--enrich-geo`)
- [ ] ASN lookup (`--enrich-asn`)
- [ ] Risk scoring per event

### v1.2 AI Assist
- [ ] Unknown log format detection via LLM
- [ ] Plain-English log summarization
- [ ] MITRE ATT&CK tactic tagging
- [ ] `lognorm explain` powered by AI

### v2.0 Extended Platform
- [ ] journald support
- [ ] Auditd support
- [ ] Windows Event Log support
- [ ] Web UI for log visualization
- [ ] Timeline view across multiple log files

---

## Contributing

Contributions are welcome, especially new parser modules.

```bash
# Fork and clone
git clone https://github.com/ethic-bakeery/lognorm.git
cd lognorm

# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run against a real log
lognorm analyze /var/log/auth.log
```

When contributing a new parser, include at minimum: 10 fixture log lines covering format variations, unit tests for each variation, and field mapping documentation in the PR description.

---

## Why Not Just Use...

| Tool | The Problem |
|---|---|
| **Logstash** | Heavy infrastructure, requires Elastic stack, overkill for local analysis |
| **Grok** | Regex-centric, requires knowing the format before you can parse it |
| **lnav** | Viewer only, no structured export, no detection |
| **grep / awk** | Powerful but requires format knowledge and produces unstructured output |
| **Splunk** | Enterprise cost, not CLI-native, not analyst-portable |

LogNorm occupies a specific gap: **fast, local, structured, zero-config log normalization** for analysts who need answers now.

---

*LogNorm -> Because your logs deserve structure, and your analysts deserve speed.*
