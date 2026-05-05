# Can't Prompt Your Way Through This: Designing Security Challenges Robust Against AI Agents

## Status
- [x] Draft  [ ] Submitted  [ ] Accepted  [ ] Delivered

## Target conferences
- C3 / CCC Congress — CFP deadline: ~September
- Insomni'hack — CFP deadline: ~December
- No Hat — CFP deadline: ~July
- Hack.lu — CFP deadline: ~July
- DeepSec — CFP deadline: ~August

## Format
Duration: 40 min | Type: talk (or 2h workshop if accepted in that format)

## Abstract (public-facing, ~300 words)

AI coding agents — ChatGPT, Claude Code, Gemini CLI — can now solve introductory CTF challenges automatically. Feed a challenge description into an agent, let it spawn a shell, grep for flags, run known exploits, and iterate. For many standard CTF challenges, the agent wins before a human student has finished reading the problem statement.

This breaks a core assumption behind security education: that solving the challenge requires the student to understand the underlying concept. If an agent can solve a buffer overflow challenge without knowing what a buffer overflow is, the challenge is no longer teaching anything.

This talk presents empirical research into where and why AI agents succeed at security challenges — pattern-matched exploits, well-documented CVEs, challenges where the solution path is a few shell commands away — and where they systematically fail: multi-step reasoning chains under adversarial conditions, challenges requiring understanding of attacker intent rather than technique lookup, and scenarios built around runtime telemetry and behavioral analysis rather than static artifacts.

I then show a design methodology for security challenges that remain meaningful in the AI age. Not by blocking AI tools (that arms race is unwinnable) but by structuring challenges where following the right reasoning process is the only path to the flag. Concrete examples come from Operation Syscall Storm, a 10-level offline CTF built to teach Falco and sysdig — a domain where AI agents consistently struggle because the answers require interpreting behavioral context, not executing known techniques.

Challenge designers, educators, and CTF organizers leave with a practical framework for evaluating and improving their existing challenges.

## Extended description (for CFP committees, ~500 words)

### The Problem in Concrete Terms

Consider a standard CTF challenge: a binary with a stack buffer overflow, a known libc version, no canary, NX disabled. An AI agent with shell access can:
1. Run `file` and `checksec` on the binary
2. Identify the overflow via fuzzing or pattern matching
3. Look up ret2libc technique
4. Compute offsets with `pwntools`
5. Submit the flag

This takes the agent under 3 minutes. A student who completes this workflow has learned nothing — they prompted, not understood. The educational value of the challenge is zero.

### Where AI Agents Fail

From testing AI agents (ChatGPT-4o, Claude Sonnet, Gemini 1.5 Pro) against a range of challenge types:

**Agents fail consistently at:**
- Challenges requiring interpretation of behavioral context (why did this process spawn this child at this time?)
- Multi-step reasoning where each step requires understanding the previous step's output, not just executing a command
- Challenges where the flag requires correctly identifying the absence of an event, not the presence of one
- Novel exploitation techniques not in training data
- Scenarios where the "correct" approach involves understanding attacker motivation rather than technique execution

**Agents succeed reliably at:**
- Pattern-matched exploitation (buffer overflows, SQL injection, known web vulns)
- Reverse engineering with known packers or standard algorithms
- Challenges where flag format is predictable and greppable
- Any scenario reducible to "run this tool and read the output"

### The Operation Syscall Storm Case Study

Operation Syscall Storm is a 10-level offline CTF where every challenge is grounded in Falco and sysdig telemetry. Players are analysts hunting "The Phantom" — a threat actor whose trail exists only in syscall captures and Falco rule output.

When we tested AI agents against these challenges:
- Levels 1–3 (basic syscall reading): agents solved these with moderate success
- Levels 4–7 (behavioral pattern identification, rule writing): agents struggled — they could generate Falco rule syntax but couldn't reason about what behavioral pattern the evidence implied
- Levels 8–10 (multi-event correlation, attacker intent reconstruction): agents consistently failed — these require building a mental model of attacker decision-making from incomplete evidence

The common factor in agent-resistant challenges: **the answer requires reasoning about behavioral context, not executing a known technique**.

### Design Methodology

Five principles for AI-resistant challenge design:

1. **Context dependency:** The flag requires interpreting multiple pieces of evidence in relation to each other, not finding a single indicator
2. **Behavioral reasoning:** The solution involves answering "why did this happen" not "what command produces this output"
3. **Novel scenario construction:** The attack pattern should not be directly in AI training data
4. **Adversarial framing:** Present the challenge from the defender's perspective — what is the attacker's intent?
5. **Process over product:** Design scoring to reward demonstrated understanding, not just correct flags

### Educational Impact

This talk is ultimately about maintaining the educational value of security training in an era where AI tools can shortcut technique-based learning. The goal is not to restrict AI tool use but to design challenges where using AI as a crutch produces wrong answers — because understanding is the only path to the correct one.

## Key takeaways
1. Empirical data on where AI agents succeed and fail at security challenges — the failure modes reveal what good challenge design looks like
2. A five-principle methodology for designing security challenges that test understanding, not AI prompt quality
3. Concrete examples from Operation Syscall Storm showing behavioral/contextual challenges that AI agents consistently fail

## Audience
CTF organizers, security educators, blue team trainers, and anyone designing security exercises or curricula. Also relevant to security researchers interested in AI agent capabilities and limitations.

## Prerequisites
Familiarity with CTF challenges or security training scenarios. No AI or Falco background required.

## Demo / materials
- Operation Syscall Storm CTF: `ctf-ai/` (to be published after `make build-all`)
- Challenge examples with AI agent transcripts showing failure modes
- Design checklist: Markdown template for evaluating existing challenges

## Speaker notes
- CCC framing: lead with the educational/societal angle — "what does it mean for security education when AI solves the exercises?"
- Insomni'hack framing: the conference has its own CTF — pitch the methodology as something the organizers can use
- The AI agent failure transcript is the most compelling demonstration — show a capable model confidently producing the wrong answer because it looked up a technique instead of reasoning
- Workshop version: participants evaluate their own CTF challenges using the five-principle framework and redesign one challenge live
- Don't frame this as "AI bad" — frame it as "here's what we learn about challenge design from AI behavior"
