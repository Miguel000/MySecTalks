# Hook Before You Look: Intercepting AI Coding Agent Tool Calls Before Execution

## Status
- [x] Draft  [ ] Submitted  [ ] Accepted  [ ] Delivered

## Target conferences
- troopers — CFP deadline: ~October
- DeepSec — CFP deadline: ~August
- 44CON — CFP deadline: ~June
- Insomni'hack — CFP deadline: ~December

## Format
Duration: 40 min | Type: talk with live demo

## Abstract (public-facing, ~300 words)

Falco monitors syscalls — what the OS sees after an action happens. But AI coding agents declare their intent before execution, through tool-call APIs like Claude Code's PreToolUse hooks. In this talk I present an architecture that intercepts those hooks in user space, evaluates them against Falco rules via a custom Rust plugin, and enforces deny/ask/allow verdicts before a single byte hits the filesystem.

I show five attack classes that are completely invisible to kernel instrumentation: sandbox-disable parameters passed per tool call, MCP server installation commands issued through the agent, API base URL overrides that silently redirect traffic to attacker infrastructure, settings.json poisoning to inject persistent hooks, and per-command hook bypass flags. For each, I demonstrate the attack and the enforcement block.

The result is a layered detection model: hooks catch agent intent before execution; syscalls catch execution consequences after the fact. Neither alone is sufficient — kernel monitoring is blind to what the agent decided to do; hook monitoring is blind to what processes outside the agent are doing. I show where each layer is essential and where they overlap.

All source code and detection rules are released under Apache 2. Attendees leave with a working architecture they can deploy to protect any AI coding agent that exposes a hook API.

## Extended description (for CFP committees, ~500 words)

### Background

AI coding agents are now standard tooling in software development teams. Claude Code, GitHub Copilot, Cursor, Aider, and similar tools execute shell commands, read and write files, modify configuration, and install packages — often with minimal oversight. As adoption grows, attackers are following: malicious MCP servers, prompt injection chains, settings poisoning, and sandbox escape techniques are being actively developed and deployed.

The standard response has been to apply runtime security monitoring at the kernel layer using tools like Falco. This works well for detecting post-execution behavior — a shell spawned by an agent, a credential file accessed, a network connection established. But there is a fundamental gap: by the time the kernel sees the action, it has already happened.

### The Hook Layer

Claude Code and similar agents expose a pre-execution hook API: before any tool call is executed, an external process can inspect the call and return allow, deny, or ask-the-user. This hook is the only place where certain attacks are detectable:

- `dangerouslyDisableSandbox: true` passed as a per-tool-call parameter — no syscall fires until after the sandbox is already bypassed
- `claude mcp add attacker-server` — the agent is about to install a malicious MCP server; kernel only sees the npm process that follows
- `ANTHROPIC_BASE_URL` override injected mid-session — the next API call goes to the attacker; kernel sees a normal HTTPS connection

### Architecture

The system consists of:
- A Falco plugin written in Rust that receives hook events via Unix socket
- An embedded broker (HTTP server + socket listener) that translates hook payloads to Falco event format
- A rule set covering 28+ hook-specific attack patterns organized into three categories: sandbox disabling, MCP/supply chain threats, and persistence mechanisms
- A verdict returned to the agent before the tool call executes

The plugin operates entirely without elevated privileges — no kernel modules, no eBPF, no root required.

### Detection Rules Covered

- Sandbox disable via `dangerouslyDisableSandbox` parameter
- MCP server installation via `claude mcp add`
- `npx -y` execution (silent package install)
- Write to `.claude/commands/` outside the working directory (persistent backdoor)
- Write to `CLAUDE.md` outside the working directory (instruction injection)
- API base URL override (traffic interception)
- API key written to `.env` file
- Known IOC domain patterns (341 domains from the ClawHavoc campaign)
- Base64-encoded commands in MCP config
- Settings.json hook injection

### Key Takeaway

This talk establishes that hook-level and kernel-level detection are complementary, not redundant. Teams deploying AI coding agents need both layers. The tooling to add the hook layer is open source and deployable in minutes.

## Key takeaways
1. Five attack classes against AI coding agents are invisible to syscall-level monitoring — hook interception is the only detection point
2. A working Rust plugin + Falco rules architecture enforces agent policies at pre-execution, not post-execution
3. The two-layer model (hooks + syscalls) is the minimum viable detection stack for AI agent deployments

## Audience
Security engineers, DevSecOps practitioners, and anyone deploying AI coding agents in their development workflow. Blue team and detection engineering focus.

## Prerequisites
Basic familiarity with Falco or runtime security concepts. No Rust knowledge required.

## Demo / materials
- OSS repo: `coding-agents-kit/` (to be published)
- Supporting blog: coding-agents-kit architecture post (draft)

## Speaker notes
- Live demo: show Claude Code blocked mid-session when attempting to install a malicious MCP server
- Emphasize: "not Sysdig product, this is an architecture you can build with OSS components"
- Have fallback recorded demo in case live network is flaky
- The "attacks invisible to kernel monitoring" framing is the strongest hook — lead with that
