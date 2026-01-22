# CLAUDE.md
**Agent Protocol for Claude Code**

## 🤖 Agent Registry
| Role | Resp | Path |
| :--- | :--- | :--- |
| **Orchestrator** | **Orchestrator**. Start here. | `.agents/orchestrator/AGENT.md` |
| **Planner** | **Thinking**. Specs, Arch, Plans. | `.agents/planner/AGENT.md` |
| **Reviewer** | **Quality**. Sec, Perf, Refactor. | `.agents/code_reviewer/AGENT.md` |
| **Tester** | **Verify**. Plans, Auto-tests. | `.agents/tester/AGENT.md` |
| **DevOps** | **Ops**. Git, CI/CD, Docker. | `.agents/devops/AGENT.md` |
| **Security** | **Sec**. SBOM, Threat Model. | `.agents/security/AGENT.md` |
| **UI/UX** | **Design**. Styles, Palettes. | `.agents/ui_ux/AGENT.md` |
| **Writer** | **Docs**. API, Guides. | `.agents/tech_writer/AGENT.md` |

## 🛠️ Skills Registry
| Skill | When to Use | Priority |
| :--- | :--- | :--- |
| [brainstorming](.claude/skills/brainstorming/SKILL.md) | Before ANY creative work | 🔴 First |
| [writing-plans](.claude/skills/writing-plans/SKILL.md) | After design approval, before coding | 🔴 First |
| [executing-plans](.claude/skills/executing-plans/SKILL.md) | When you have a plan to execute | 🟠 Second |
| [test-driven-development](.claude/skills/test-driven-development/SKILL.md) | ALL code changes | 🔴 First |
| [systematic-debugging](.claude/skills/systematic-debugging/SKILL.md) | ANY technical issue or bug | 🔴 First |
| [requesting-code-review](.claude/skills/requesting-code-review/SKILL.md) | After tasks, before merge | 🟠 Second |
| [frontend-design](.claude/skills/frontend-design/SKILL.md) | Building web UIs | 🟠 Second |
| [explaining-code](.claude/skills/explaining-code/SKILL.md) | Teaching, explaining code | 🟢 Optional |

> **Full Index:** [.claude/skills/SKILL_INDEX.md](.claude/skills/SKILL_INDEX.md)

## 📂 Artifact Standards
| Type | Path | Owner |
| :--- | :--- | :--- |
| **Specs** | `specs/` | Planner |
| **Design** | `design/` | Planner |
| **Docs** | `docs/` | Writer |
| **Tests** | `tests/` | Tester |
| **Sec** | `security/` | Security |
| **Standards** | `.agents/STANDARDS.md` | **ALL** |
| **State** | `.agents/SCRATCHPAD.md` | **ALL** |

## 🧠 Claude-Specific Protocol
1.  **Subagent Pattern**: Use `Task` tool to spawn specialized agents. Pass Agent path as context.
    ```
    Task: "Read .agents/planner/AGENT.md and act as the Planner. Create specs for [feature]."
    ```
2.  **Parallel Execution**: Use `Task` tool with `TodoWrite` to define non-blocking subtasks.
3.  **State Sync**: Read/Write `.agents/SCRATCHPAD.md` before/after major steps.
4.  **File Focus**: Claude Code works best with explicit file paths. Always specify paths.

## ⚡ Quick-Start
```bash
# 1. User Request
"Build a login feature"

# 2. Orchestrator Starts
Read CLAUDE.md -> Initialize SCRATCHPAD -> Spawn Planner

# 3. Planner Thinks
Write specs/login.md -> Write design/login_arch.md -> Output task list

# 4. Orchestrator Executes
Assign tasks to Coder -> Review -> Test -> Deploy
```
