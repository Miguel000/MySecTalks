# Your CI Pipeline Is a Target: 13 Supply Chain Attack Patterns Falco Catches

## Status
- [x] Draft  [ ] Submitted  [ ] Accepted  [ ] Delivered

## Target conferences
- troopers — CFP deadline: ~October
- DeepSec — CFP deadline: ~August
- 44CON — CFP deadline: ~June
- BotConf — CFP deadline: ~August

## Format
Duration: 40 min | Type: talk with demo

## Abstract (public-facing, ~300 words)

Software supply chain attacks have moved into CI/CD pipelines. Attackers compromise dependencies, inject malicious GitHub Actions, steal secrets from runners, and pivot from build infrastructure to production cloud accounts. The tooling to detect these attacks at runtime exists — but out-of-the-box Falco coverage leaves most of the attack surface unmonitored.

We analyzed 23 supply chain attack patterns against GitHub Actions pipelines and measured Falco detection coverage: 9% fully covered, 35% partially covered, 57% with no detection at all. Those 13 undetected patterns include some of the most dangerous attack techniques in modern supply chain compromise.

This talk presents each of the 13 patterns: npm token theft combined with autonomous `npm publish` for self-propagation, Python `.pth` file persistence injected through malicious `setup.py` during `pip install`, `LD_PRELOAD` injection via CI runner environment variables, OIDC token theft pivoting to AWS credentials via STS exchange, self-hosted runner backdoor registration via GitHub API, ICP Canister C2 beaconing using censorship-resistant domains, and six more.

For each pattern I show the attack technique, the Falco rule I wrote to close the gap, and why the coverage gap exists in generic rulesets. Defenders leave with 13 production-ready rules and a mental model for auditing their own CI detection coverage.

## Extended description (for CFP committees, ~500 words)

### The Coverage Gap Problem

Falco ships with excellent general-purpose detection rules. They catch shell escapes, privilege escalation, credential file access, and reverse shells. But GitHub Actions pipelines create an environment where many standard heuristics break down:

- Runners install packages constantly — `pip install` and `npm install` are expected behavior, making persistence via `setup.py` hard to distinguish from legitimate builds
- Runners have broad cloud credentials — `aws sts get-caller-identity` is normal; `aws sts assume-role` pivoting to a different account is not
- Runners spawn many processes — a shell spawned by a build step looks identical to a shell spawned by a malicious action

Generic Falco rules were not written with this context. They produce either too many false positives (blocking legitimate builds) or too many false negatives (missing CI-specific attack patterns).

### The 13 Patterns

**Self-propagating supply chain:**
- npm token theft + `npm publish` to spread malware to dependents
- PyPI token theft + `twine upload` for the same pattern in the Python ecosystem

**Persistence in build artifacts:**
- Python `.pth` file written via `setup.py` (persists into installed virtualenvs)
- `NODE_OPTIONS=--require` pre-loading malicious scripts in all Node processes

**Credential pivoting:**
- OIDC token exchange to AWS STS — token is legitimate, pivot is not
- Environment variable dump to external service (curl to webhook)

**Runner compromise:**
- Self-hosted runner registration backdoor via GitHub API
- `LD_PRELOAD` injection via CI runner environment variable

**Exfiltration and C2:**
- ICP Canister domain beaconing (censorship-resistant C2 infrastructure)
- DNS exfiltration via crafted subdomain lookups
- Source code archive exfiltration to S3 or object storage

**Action tampering:**
- Pinned Action SHA replacement via workflow file write
- Secrets written to workflow outputs (leaked to logs)

### The Detection Rules

Each of the 13 patterns has a corresponding Falco rule. The rules were designed to minimize false positives in real CI environments by:

- Scoping detection to process trees originating from runner processes
- Using allowlists for expected package managers vs. unexpected registry endpoints
- Combining process ancestry with network destination for C2 detection

All 13 rules are released as OSS with example `falco.yaml` configuration for GitHub Actions self-hosted runner deployments.

### Methodology Note

The gap analysis methodology is itself transferable. The talk documents how to systematically evaluate Falco rule coverage against a threat model: enumerate attack patterns, map to rule conditions, test with synthetic events, classify coverage. Teams can use this methodology to audit their own Falco deployments.

## Key takeaways
1. 57% of analyzed CI/CD supply chain attack patterns have no detection in out-of-the-box Falco — the specific gap is now documented
2. 13 Falco rules that close the identified gaps, production-ready for GitHub Actions self-hosted runner deployments
3. A methodology for auditing Falco rule coverage against any threat model

## Audience
DevSecOps engineers, security architects, and defenders responsible for CI/CD pipeline security. Relevant to anyone running GitHub Actions, especially with self-hosted runners.

## Prerequisites
Basic familiarity with CI/CD concepts (pipelines, runners, secrets). Falco experience not required.

## Demo / materials
- OSS rules: `falco-actions/rules/falco_cicd_rules.yaml` (to be published)
- Coverage analysis document: full mapping of 23 patterns to Falco rules
- Supporting blog: CI/CD supply chain detection gaps

## Speaker notes
- Open with the coverage numbers — 9% / 35% / 57% — as the hook; concrete stats land well
- Demo: show a self-hosted runner getting compromised via OIDC pivot, then show the Falco alert from the new rule
- The "why does the gap exist in generic rules" explanation is important for credibility — don't skip it
- troopers audience: emphasize the enterprise deployment guidance and the NIS2 supply chain compliance angle
