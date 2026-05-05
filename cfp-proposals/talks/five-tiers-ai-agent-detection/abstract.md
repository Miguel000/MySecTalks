# Five Tiers of Threat: A Detection Framework for AI Coding Agents

## Status
- [x] Draft  [ ] Submitted  [ ] Accepted  [ ] Delivered

## Target conferences
- C3 / CCC Congress — CFP deadline: ~September
- Hack.lu — CFP deadline: ~July
- No Hat — CFP deadline: ~July
- Pass The Salt — CFP deadline: ~March

## Format
Duration: 45 min | Type: talk or workshop (both versions prepared)

## Abstract (public-facing, ~300 words)

As AI coding agents become standard developer tooling, attackers are following. This talk presents a 5-tier threat model — installation, runtime behavior, active exploitation, supply chain / MCP skills, and secrets exfiltration — built from 6 months of threat research across Claude Code, Gemini CLI, Aider, Cursor, and Codex.

I map 136 detection rules to MITRE ATT&CK across 23 techniques, walk through real attack chains — prompt injection leading to RCE, a malicious MCP server harvesting credentials, CVE-2026-25253 (WebSocket origin bypass in OpenClaw enabling unauthenticated command execution) — and explain the design decisions behind each rule. Why do behavioral patterns outperform signatures for agent threats? How do time-based correlations cut false positives when detecting credential theft? Where do honest gaps remain that no rule can close?

Falco is used as the detection engine throughout. All 136 rules, the threat model template, and the MITRE mapping are released as OSS. The goal is not just to share the rules but the methodology — so defenders can extend it as new agents and new attack techniques emerge.

Attendees leave with a structured threat model for AI agents, a ready-to-deploy rule set, and the reasoning process to build new rules when the next threat appears.

## Extended description (for CFP committees, ~500 words)

### Why Now

Every major development team is adopting AI coding agents. These agents have filesystem access, shell execution, network connectivity, and package management capabilities. They run with developer-level privileges. They accept natural language instructions that can be manipulated. And they are being targeted.

The security community has not produced a comprehensive threat model for this attack surface. Individual CVEs get patched; individual attack patterns get rules written for them. But there is no systematic framework covering the full threat lifecycle from first installation through active exploitation through exfiltration.

### The Five-Tier Model

**Tier 1 — Installation Detection:** How does an AI agent arrive on a system? npm global installs, pip packages, binary downloads, brew formulae. Detection focuses on unusual install sources, unsigned binaries, and first-run behaviors. ~15 rules.

**Tier 2 — Runtime Behavior:** What does a legitimate agent do versus a compromised or manipulated one? Baseline profiling, anomalous file access patterns, unexpected network destinations. ~35 rules.

**Tier 3 — Active Exploitation:** Prompt injection leading to code execution, reverse shells spawned by agent processes, privilege escalation attempts, CVE-2026-25253 WebSocket origin bypass. ~40 rules.

**Tier 4 — Supply Chain / MCP Skills:** Malicious skill installation, known IOC domains in MCP configs, ClawHavoc campaign indicators (341 malicious skills), CVSS 10/10 MCP server vulnerabilities. ~30 rules.

**Tier 5 — Secrets Exfiltration:** Agent processes accessing credential files, cloud token reads followed by outbound connections, API key patterns in spawned process arguments. ~20 rules.

### Rule Design Methodology

Three design principles guided every rule:

1. **Behavioral over signature:** Signatures age out as attackers adapt. Rules that describe behavioral anomalies (agent process accessing `/etc/shadow`, shell spawned as child of coding agent binary) survive attacker iteration better.

2. **Time correlation for precision:** A single credential file read may be legitimate. A credential file read within 5 minutes of an unknown skill installation followed by an outbound connection is not. Time-windowed correlations dramatically reduce false positives in Tier 4–5 rules.

3. **Honest about gaps:** Some threats cannot be detected at the syscall layer. The talk documents these gaps explicitly — not to leave defenders hopeless, but to show where compensating controls (hook-level detection, network segmentation, least-privilege) are necessary.

### Release

All 136 rules are released under Apache 2 with full MITRE mapping and a threat model template in Markdown. The rules are validated against Falco 0.43+ and tested with a purpose-built harness that generates synthetic agent activity.

## Key takeaways
1. A structured 5-tier threat model covering the full AI agent attack lifecycle, from installation to exfiltration
2. 136 Falco detection rules with MITRE ATT&CK mapping, ready to deploy
3. A rule design methodology — behavioral patterns + time correlations — that survives attacker iteration

## Audience
Security engineers, blue teams, DevSecOps practitioners, and anyone building detection for AI agent deployments. Prior Falco experience is helpful but not required.

## Prerequisites
Basic understanding of Linux process execution and syscall concepts. No Falco experience required.

## Demo / materials
- OSS rules: `Projects/ai-agent-falco-research/` + `Projects/strt_threat_detection/AIAgents/` (to be published)
- Supporting blog: threat model post (draft)
- Threat model template: Markdown format for reuse

## Speaker notes
- Workshop version: 3-hour hands-on where attendees write one rule per tier using a Falco sandbox VM
- Talk version: walk through one complete attack chain per tier (5 chains, ~7 min each)
- Don't oversell completeness — the "honest about gaps" section builds credibility
- The CVE-2026-25253 example is the most compelling Tier 3 demonstration — demo it if possible
