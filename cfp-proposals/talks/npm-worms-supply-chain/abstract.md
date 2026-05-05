# Shai-Hulud: When npm Packages Become Self-Replicating Worms

## Status
- [x] Draft  [ ] Submitted  [ ] Accepted  [ ] Delivered

## Target conferences
- Pass The Salt — CFP deadline: ~March
- C3 / CCC Congress — CFP deadline: ~September
- No Hat — CFP deadline: ~July
- BotConf — CFP deadline: ~August

## Format
Duration: 40 min | Type: technical talk

## Abstract (public-facing, ~300 words)

Typosquatting is the entry-level threat in the npm ecosystem: publish a lookalike package, wait for developers to mistype a name, collect whatever the install hook can grab. Shai-Hulud is different. It does not wait.

Shai-Hulud is a self-replicating worm that spreads through npm. Once a developer installs a compromised package, the worm infects the local development environment, harvests npm authentication tokens and CI secrets, and uses those credentials to publish poisoned versions of the victim's own packages to the registry — spreading to every downstream developer who updates their dependencies. The attack propagates exponentially through the dependency graph.

This talk covers the full attack lifecycle: initial compromise via a seemingly legitimate package with a malicious install hook, the infection mechanics that make the worm persistent across development sessions, credential harvesting from npm tokens and CI pipeline secrets, and the autonomous propagation step that makes this categorically different from static supply chain attacks.

I show why existing package security tooling — npm audit, Snyk, Dependabot — fails to detect the worm phase (the published packages are signed with legitimate credentials and contain real functionality). I then show what syscall-level monitoring with Falco catches that static analysis misses: unexpected network connections during package install, credential file reads by install scripts, processes spawning shells during dependency resolution.

The goal is to make sure developers understand not just typosquatting but the worm threat that emerges the moment an attacker gains a foothold inside a build environment.

## Extended description (for CFP committees, ~500 words)

### Why This Is Different From Typosquatting

Typosquatting requires waiting for victims to make a mistake. At best, an attacker reaches a fraction of developers who mistype a specific package name. Shai-Hulud breaks this constraint: once a single developer is infected, their legitimate package publishing credentials become the propagation vector. The worm reaches every developer who installs any package the victim maintains.

This changes the threat model fundamentally:
- No typo required — the worm spreads through legitimate, trusted packages
- The worm is signed with the victim's legitimate npm token — traditional supply chain verification passes
- The propagation is exponential through the dependency graph
- Detection requires behavioral analysis, not static indicators

### Attack Lifecycle

**Stage 1 — Initial Compromise:**
An npm package with a malicious `postinstall` hook is published. The hook runs automatically during `npm install` with the executing user's permissions. It profiles the environment, identifies npm authentication tokens in `~/.npmrc` and CI environment variables, and installs a persistent backdoor.

**Stage 2 — Credential Harvest:**
The backdoor harvests credentials on a schedule: npm tokens, npm two-factor authentication bypass tokens (when stored in config), AWS credentials (common in developer environments), CI secrets exposed via environment variables during local builds.

**Stage 3 — Autonomous Propagation:**
Using harvested npm tokens, the worm publishes malicious minor versions of the victim's own packages. The new versions include the worm payload alongside the original functionality. Since the package comes from the legitimate maintainer, it passes maintainer verification checks.

**Stage 4 — Downstream Infection:**
Developers who have the victim's packages as dependencies and run `npm update` install the infected version. Their environments are now Stage 1 for the next wave.

### Detection with Falco

Static analysis tools fail here because:
- Install hooks are expected to run arbitrary code
- The published packages contain real, legitimate functionality
- npm tokens used for publishing are legitimate

Runtime monitoring catches what static analysis cannot:
- **Network connection during `npm install`:** Expected for downloading packages; unexpected for phoning home to an attacker domain
- **Credential file read by install script:** `~/.npmrc` read by a `node` process spawned from a package install hook — anomalous
- **Shell spawned during dependency resolution:** `sh -c` as a child of `npm install` with unusual arguments
- **`npm publish` executed outside of a CI pipeline:** During a build step that has no publish step in its configuration

### Runtime Detection Rules

Three Falco rules covering this attack:
1. `Suspicious credential access during package install` — triggers on `~/.npmrc`, `~/.aws/credentials`, `~/.ssh/id_*` reads by npm install child processes
2. `Unexpected network connection during npm install` — triggers on non-registry outbound connections during dependency resolution
3. `npm publish executed from development environment` — triggers on `npm publish` outside expected CI process ancestry

## Key takeaways
1. Self-replicating npm worms are categorically different from typosquatting — the propagation mechanic means a single victim can infect their entire downstream dependency graph
2. Static supply chain security tools (audit, Dependabot) do not detect the worm phase — runtime behavioral monitoring is the necessary complementary layer
3. Three concrete Falco rules that detect worm behavior at install time, before propagation begins

## Audience
Developers, DevSecOps practitioners, and anyone who publishes or consumes npm packages. Security researchers interested in supply chain threats.

## Prerequisites
Basic familiarity with npm and package management. No security background required — this talk teaches the threat from first principles.

## Demo / materials
- OSS detection rules: `falco-actions/rules/` (supply chain rules)
- Supporting blog: Shai-Hulud worm research (published T3chfest 2026 — this is the expanded international version)
- Demo environment: Docker-isolated npm environment with Falco monitoring

## Speaker notes
- This was presented at T3chfest 2026 in Spanish — this is the expanded English version for international audiences
- BotConf framing: lead with the worm mechanics and propagation graph (malware research angle)
- Pass The Salt framing: lead with the OSS detection tooling and Falco rule release
- The demo is Docker-isolated: safe to run live
- "Shai-Hulud" is the name in the Sysdig blog post — use consistently, explain the Dune reference briefly
