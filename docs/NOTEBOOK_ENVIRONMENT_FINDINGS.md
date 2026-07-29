# Notebook environment: findings and recommendations

*Compacted from research reviewed 28 July 2026. Claims checked against primary docs unless noted.*

## Verdict

**Self-host JupyterHub** (VM with [TLJH](https://tljh.jupyter.org/), or [Zero to JupyterHub](https://z2jh.jupyter.org/) on managed K8s) with a pinned course image. The teaching team can run the necessary ops; a managed classroom SaaS is **out of scope**. Keep Jupyter as the durable workspace; use **Marimo for new interactive lessons** inside that Hub. Put assessment and the course `@Tutor` in **external services**—not in a default coding agent.

---

## Recommendations (decision order)

1. **Workspace:** Self-hosted JupyterHub + JupyterLab—one isolated server per learner, OAuth allow-list, idle cull, HTTPS, backups, pinned image (`pandas` / sklearn / course data). Start with **TLJH on a single VM** for the pilot (~10–100 users); move to **Z2JH on managed K8s** if you need tighter resource isolation, rolling image deploys, or headroom beyond one box.
2. **Teaching medium:** Prefer **Marimo** for new beginner-facing interactive lessons (EDA, parameter exploration, reactive public tests). Keep existing `.ipynb` lessons on Jupyter until converted deliberately—order-dependent notebooks need restructuring ([convert docs](https://marimo.io/for-educators)).
3. **AI tutor:** Course-owned **`@Tutor` / `@HomeworkTutor` backend** (Hub Service or sidecar) with a course-paid key, hint-first policy, logging, and human escalation. Do **not** make Claude Code / Codex CLI / Marimo Agent the default learner tutor.
4. **Homework:** Source-of-truth assignment repo → sanitized learner copy → immutable snapshot → sandboxed autograde → feedback draft. Start with **nbgrader** on Hub; design the feedback worker I/O as platform-neutral; trial **Otter** (and optionally [Classroom 50](https://github.com/foundation50/classroom50/)) for take-home with hidden tests.
5. **Fallback / practice:** molab (Marimo) or Colab for zero-ops demos—not the assessed path.
6. **Pilot (10–20 learners):** one Jupyter lesson + constrained tutor; one Marimo conversion; score time-to-first-success, support tickets, over-help incidents, tutor cost/review rate.

---

## Findings by option

| Option | Multi-user classroom | Beginner setup | Course-owned tutor | Assessed homework | Fit |
| --- | --- | --- | --- | --- | --- |
| **JupyterHub + JupyterLab** (self-hosted VM or K8s) | Excellent (per-user server; TLJH 0–100; Z2JH at scale) | Excellent browser-first | Custom persona *possible*; default Jupyter AI v3 path is coding agents—prefer external `@Tutor` | nbgrader native; Otter portable | **Chosen platform** |
| **Marimo on Hub** | Good via [JupyterLab extension](https://docs.marimo.io/guides/deploying/jupyterhub/) | Good; `--sandbox` pins packages in the notebook | Built-in Ask/Manual good for exploration; Agent/Pair too powerful for assessment | Incomplete alone—fork/download + external grader | **Preferred new lesson format** |
| **molab / WASM** | No Hub accounts | Best zero-install | No protected course backend | Download to Gradescope/etc. | Practice / demos |
| **Colab / Codespaces** | Not course-owned; account limits | Very good | Provider AI; weak pedagogy control | Weak / DIY | Fallback only |
| Deepnote / CoCalc / 2i2c | Managed / SaaS | — | — | — | **Not needed** (team will ops the Hub) |

### Grounding notes (validated)

- **JupyterHub** spawns a separate server per user; TLJH targets small classes on one VM; Z2JH is the K8s path ([overview](https://jupyterhub.readthedocs.io/en/latest/), [TLJH](https://tljh.jupyter.org/), [Z2JH](https://z2jh.jupyter.org/)).
- **Marimo:** reactive pure-Python notebooks; educator FAQ covers molab share links, download submission, `--sandbox`, pytest cells, Jupyter conversion caveats ([Teach with marimo](https://marimo.io/for-educators), [teaching methods](https://marimo.io/guidelines)). Hub integration and sandbox via extension are documented ([JupyterHub guide](https://docs.marimo.io/guides/deploying/jupyterhub/)).
- **Marimo AI:** Manual / Ask / Agent / Code modes; custom rules; providers need credentials or local models; AI surfaces can be hidden (`[ai] enabled = false`). Agent panel is **experimental**; custom ACP agents “coming soon”; `marimo pair` grants full notebook/runtime access ([AI completion](https://docs.marimo.io/guides/editor_features/ai_completion/), [agents](https://docs.marimo.io/guides/editor_features/agents/), [pair](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/)).
- **Jupyter AI v3:** ships **with no agent by default**; personas are primarily installed ACP CLIs (Claude Code, Codex, Copilot CLI, …) with MCP/tools and permission prompts. Custom personas via entry points remain available, but the product direction is frontier coding agents—not a hint-first course tutor ([getting started](https://jupyter-ai.readthedocs.io/en/stable/getting-started.html), [developer API](https://jupyter-ai.readthedocs.io/en/stable/developers/index.html), [v3 release notes](https://github.com/jupyterlab/jupyter-ai/issues/1531)).
- **Classroom 50:** free GitHub Classroom alternative; state lives in a GitHub Team/Enterprise org (Education may cover teachers); push → Actions → `submit/<timestamp>-<sha>` → Release + `result.json`. Teachers must be signed in for some admin actions (no always-on app server). Grading/publishing share one Actions job—not a secrets isolation boundary ([wiki](https://github.com/foundation50/classroom50/wiki), [Autograders](https://github.com/foundation50/classroom50/wiki/Autograders)).
- **nbgrader / Otter:** nbgrader = Hub-native release/collect/Formgrader/HTML feedback; Otter = sanitized notebook + container/Gradescope bundle + CSV—better portable boundary for an async feedback worker ([nbgrader](https://nbgrader.readthedocs.io/), [Otter](https://otter-grader.readthedocs.io/), [Berkeley DataHub Otter note](https://curriculum-guide.datahub.berkeley.edu/support/troubleshooting/otter-grader)).
- **Comparable practice:** Berkeley DataHub = JupyterHub browser-first day one ([curriculum guide](https://curriculum-guide.datahub.berkeley.edu/technology/introduction-to-jupyter/)). Content-in-Git + hosted runtime remains the durable pattern (e.g. Hugging Face course notebooks from Git).

### Corrections to the long research note

| Claim in research | Assessment |
| --- | --- |
| Managed SaaS (Deepnote / 2i2c) as fallback if ops is hard | **Not applicable here**—team will run Hub on VM or managed K8s. |
| Jupyter AI v3 is an “excellent” fit for a course `@Tutor` persona | **Overstated.** Personas/MCP exist, but v3 defaults to **coding agents** that complete work. A pedagogic tutor needs a **custom package or external Hub Service**. |
| Deepnote packages “do not comprehensively handle hundreds of submissions” | **Unsupported** in Deepnote docs (and moot if Deepnote is not used). |
| Classroom 50 push → immutable tag → `result.json` | **Correct** (tag + Release + `result.json` contract). |

---

## Architecture sketch

```text
VM (TLJH) or managed K8s (Z2JH)
        │
Browser → JupyterHub login → isolated JupyterLab
                           ├─ pinned course image + lessons/data
                           ├─ Marimo extension (new reactive lessons)
                           ├─ optional constrained in-editor helper (read-only)
                           └─ assessed work → snapshot → Otter/nbgrader sandbox
                                                      → @HomeworkTutor (Hub Service)
                                                      → Slack DM + human queue
```

**Ops baseline (team-owned):** HTTPS, OAuth allow-list, per-user CPU/RAM limits, idle cull, home-directory persistence, image rebuild between cohorts, backups, and a disposable network-restricted grader—not the Hub control plane.

**Tutor policy (non-negotiable):** diagnostic question → hint ladder → refuse final exercise answer; read-only tools by default; cite lesson; escalate to human; never expose hidden tests/solutions; human is final grader ([OpenAI assessment guidance](https://help.openai.com/en/articles/8313397-how-can-chatgpt-be-used-for-assessment-and-feedback)).

**Slack:** notification + handoff only (Events API / app), not the gradebook. Map Slack identity to Hub identity via explicit OAuth; no notebook contents or scores in public channels.

---

## Gaps the long note underplayed (important for PyLadies)

1. **Deploy path choice.** TLJH-on-VM is enough for a cohort pilot; plan the Z2JH cutover criteria (user count, noisy-neighbour isolation, image rollouts) up front so you do not rebuild auth/grading twice.
2. **Jupyter AI product risk.** Building `@Tutor` *inside* Jupyter AI fights v3’s ACP-agent focus; a Hub Service + model proxy is the durable bet for both Jupyter and Marimo.
3. **EU / GDPR.** Notebook + dataset content sent to hosted model providers needs a deliberate DPA/provider choice or a local/private model; minimise logging.
4. **Current course workflow.** Today: Git materials, ZIP export to Slack, local install lesson, Jupyter notebooks. The Hub must replace “install + ZIP” with **nbgitpuller / shared image**, not stack another setup step.
5. **GitHub Classroom** remains a simpler alternative to Classroom 50 if GitHub Education already covers the org; Classroom 50 wins on open tooling and the `result.json` webhook trail.
6. **Beginner Git load.** Classroom 50 / GitHub homework assumes accounts, commits, and permissions—fine as an *objective*, costly as a hidden prerequisite for week 1.
7. **AI cost & abuse.** Per-user budgets, rate limits, and an “unhelpful/unsafe” report button are required before cohort-wide rollout.
8. **Integrity.** Hidden tests check correctness, not authorship; AI policy and human review remain necessary.

---

## Suggested homework design (unchanged, still sound)

- Public checks while working; hidden robustness checks on submit.
- Run submissions in disposable, network-restricted containers; never in the Hub control plane.
- Mix auto checks with human rubric (analysis, viz, interpretation, reflection).
- `@HomeworkTutor` gets: prompt version, rubric, learner snapshot, **sanitised** test summary—never solutions or hidden tests.
- States: `queued → tests-running → preliminary-feedback-ready → revised | review-requested → human-reviewed → released`.

**nbgrader vs Otter:** nbgrader for first Hub pilot (less plumbing); Otter when portability / container boundary / Gradescope matter. Same tutor contract either way.

---

## Proof of concept checklist

- [ ] TLJH (or Z2JH) with 10–20 accounts, pinned image, one existing pandas lesson, OAuth allow-list, idle cull, HTTPS.
- [ ] Read-only course tutor as Hub Service / model proxy—measure over-help rate and €/learner.
- [ ] One Marimo lesson (EDA + reactive public tests) vs Jupyter twin on the same cohort metrics.
- [ ] One take-home through snapshot → sandbox → preliminary feedback → Slack “ready” DM.
- [ ] Decide: broaden Marimo only if learning gains beat migration and support cost; decide VM vs K8s for the next cohort.

---

## Sources

| Topic | URL |
| --- | --- |
| JupyterHub | https://jupyterhub.readthedocs.io/en/latest/ |
| TLJH | https://tljh.jupyter.org/ |
| Zero to JupyterHub (K8s) | https://z2jh.jupyter.org/ |
| JupyterHub auth | https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html |
| JupyterHub services | https://jupyterhub.readthedocs.io/en/latest/reference/services.html |
| Jupyter AI getting started | https://jupyter-ai.readthedocs.io/en/stable/getting-started.html |
| Jupyter AI developers / personas | https://jupyter-ai.readthedocs.io/en/stable/developers/index.html |
| Jupyter AI v3 direction | https://github.com/jupyterlab/jupyter-ai/issues/1531 |
| Marimo docs | https://docs.marimo.io/ |
| Marimo for educators | https://marimo.io/for-educators |
| Marimo teaching methods | https://marimo.io/guidelines |
| Marimo on JupyterHub | https://docs.marimo.io/guides/deploying/jupyterhub/ |
| Marimo AI | https://docs.marimo.io/guides/editor_features/ai_completion/ |
| Marimo agents | https://docs.marimo.io/guides/editor_features/agents/ |
| marimo pair | https://docs.marimo.io/guides/generate_with_ai/marimo_pair/ |
| nbgrader | https://nbgrader.readthedocs.io/ |
| Otter-Grader | https://otter-grader.readthedocs.io/ |
| Berkeley DataHub | https://curriculum-guide.datahub.berkeley.edu/technology/introduction-to-jupyter/ |
| Berkeley Otter note | https://curriculum-guide.datahub.berkeley.edu/support/troubleshooting/otter-grader |
| Classroom 50 | https://github.com/foundation50/classroom50/wiki |
| Classroom 50 autograders | https://github.com/foundation50/classroom50/wiki/Autograders |
| GitHub App webhooks | https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/using-webhooks-with-github-apps |
| Slack Events API | https://api.slack.com/apis/connections/events-api |
| OpenAI assessment guidance | https://help.openai.com/en/articles/8313397-how-can-chatgpt-be-used-for-assessment-and-feedback |
| Hugging Face course workflow | https://github.com/huggingface/course/blob/main/README.md |

*Long-form working notes:* [`NOTEBOOK_ENVIRONMENT_RESEARCH.md`](./NOTEBOOK_ENVIRONMENT_RESEARCH.md).
