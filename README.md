# GitScope

An MCP-powered AI agent that analyzes GitHub repositories and surfaces structured insights — built to help product managers and founders make faster, evidence-based decisions about repos they don't have time to read.

---

## Problem & Why

When evaluating a new library, vendor repo, or open-source dependency, PMs and founders typically spend 20–30 minutes manually scanning commits, issues, and PRs — and still miss key signals like maintenance gaps, bus factor risk, or stale PRs.

GitScope automates that scan and returns a structured decision brief in under a minute.

---

## What This Is

A local Python agent that uses GitHub's API + an MCP-connected LLM to generate repo health reports across three lenses: activity health, PR quality, and bug/issue signals.

---

## Architecture

```
Input: GitHub repo URL + analysis mode (health / PRs / bugs)
    ↓
GitHub API → fetch commits, PRs, issues, contributor data
    ↓
Chunked context assembly (avoids token limits for large repos)
    ↓
MCP-connected LLM (local) → structured prompt per analysis mode
    ↓
Output: Executive summary + Key findings + Risk signals + Recommended actions
```

Key files:
- `github_agent.py` — core agent logic, API calls, prompt construction
- `requirements.txt` — dependencies (Python)

---

## What It Produces

For each repo, GitScope returns:

| Section | What It Contains |
|---|---|
| Executive Summary | 2–3 sentence repo health verdict |
| Key Findings | Top 3–5 signals (commit frequency, contributor count, PR merge rate) |
| Risk Signals | Maintenance gaps, stale issues, single-contributor risk |
| Recommended Actions | Adopt / Evaluate / Avoid with reasoning |

---

## How to Use

```bash
git clone https://github.com/Ruthwik-Data/gitscope
cd gitscope
pip install -r requirements.txt
python github_agent.py --repo https://github.com/owner/repo --mode health
```

Modes: `health` | `prs` | `bugs`

---

## Lessons Learned

1. **Selective context beats full-repo dumps.** Sending all raw API data exceeded token limits and degraded output quality. Chunking by recency and relevance produced sharper summaries.

2. **Mode-specific prompts matter.** A single generic prompt produced mediocre output across all three lenses. Separate prompt templates per mode (health, PRs, bugs) improved specificity significantly.

3. **GitHub API inconsistency is a real constraint.** PR data is unreliable for repos that close issues externally or use squash merges. Any metric built on PR count alone will mislead.

---

## Known Limitations

- No quantitative benchmark yet — output quality is assessed manually, not with a formal eval
- GitHub API rate limits constrain analysis of very active repos (5000 req/hr)
- Does not yet analyze file-level code quality or test coverage
- LLM outputs vary run-to-run without temperature pinning; reproducibility is limited
- No caching — repeated analysis of the same repo re-fetches all data

---

## Why This Exists

Built as a personal productivity tool during AI stack evaluation sprints — when I needed to assess 10+ repos in a day and wanted structured, comparable output rather than ad hoc notes.

The evaluation gap it exposes: most AI developer tools optimize for code generation, not repo comprehension. This is a small step toward AI-assisted technical due diligence.

# adapted 
from - https://github.com/Shubhamsaboo/awesome-llm-apps
