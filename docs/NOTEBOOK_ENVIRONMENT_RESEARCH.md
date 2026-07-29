# Notebook environment options for the PyLadies data course

*Research snapshot: 28 July 2026.*

## Recommendation

Pilot a **browser-first JupyterHub + JupyterLab + Jupyter AI** course environment.
Give every participant an isolated, prebuilt Python workspace, accessed with a normal login. Add a course-owned **Tutor** persona to Jupyter AI; it should coach from the lesson and the learner's current notebook rather than silently completing the exercise.

Use **marimo** as a serious parallel candidate for the primary *teaching medium*—not merely as an interactive-lesson experiment—but keep JupyterHub as the account/isolation platform. Marimo now has educator-specific guidance, reactive test feedback, dependency sandboxing and a documented JupyterHub extension. It preserves the main beginner benefit: no participant-managed Python environment.

If operating a server is out of scope, evaluate **Deepnote Education** as the managed alternative. It is particularly strong for real-time group work and instructor feedback, but the browser classroom is cloud/SaaS rather than a self-hosted classroom platform. Its free Education plan currently excludes Deepnote AI; its general-purpose agent is designed to create/edit/run work, while its documented custom instructions are user-specific—not a centrally governed tutor persona. [Deepnote Education](https://deepnote.com/docs/edu-overview), [Deepnote Agent](https://deepnote.com/docs/getting-started), [custom AI instructions](https://deepnote.com/docs/custom-ai-instructions)

## Options at a glance

| Option | Multi-user self-hosting | Beginner local experience | AI tutor / custom agents | Fit |
| --- | --- | --- | --- | --- |
| **JupyterHub + JupyterLab + Jupyter AI** | Excellent: separate server/environment per learner; Google/GitHub/OAuth login possible | Excellent when browser-first; no local Python setup | Excellent: Jupyter AI v3 supports personas, custom packages, MCP and permissioned tools | **Recommended** |
| **Marimo server, preferably launched by JupyterHub** | Good through JupyterHub/Kubernetes; Marimo itself is an editor/app server, not the primary classroom identity layer | Good in browser; built-in package management; local still needs an install | Good built-in data-aware assistant and agent integration; customize prompt/provider | **Preferred for new interactive lessons** |
| **Marimo WebAssembly export** | No per-user server/account by itself; static hosting is easy | Best for zero-install, offline-friendly demos | Not a practical place for a protected, course-owned tutor backend | Great for read/modify demonstrations and lightweight exercises |
| **Deepnote Education / Cloud** | Managed cloud; public docs describe multi-tenant or dedicated single-tenant deployment, not a user-operated classroom server | Excellent: browser, shared project environment, real-time collaboration/comments | Strong built-in Agent and AI blocks; custom instructions are user-specific, and free Education excludes AI | Best no-ops pilot / group work |
| **Deepnote Open Source** | Local toolkit/editor, not yet a self-hosted browser classroom (local UI, own compute and local agent are listed on its roadmap) | Poor fit for novices: VS Code/AI-editor workflow and local environment | Local agent/BYO keys are roadmap items | Watch, but not a course platform today |
| **CoCalc / CoCalc OnPrem** | Strong: managed classroom or licensed on-prem Kubernetes/Docker deployment | Excellent browser workflow, real-time shared notebooks | Strong contextual assistant; can run a private LLM, but tutor behaviour would need custom integration/policy | Viable supported alternative to operating JupyterHub |
| Hosted notebooks (Colab/molab/Codespaces) | Lowest operations, but not self-hosted and subject to product/account limits | Very good | Provider AI features, but less control over pedagogy, data and costs | Useful fallback/demo, not the core platform |

JupyterHub is designed to spawn a separate Jupyter server for each user and is documented for small classes (The Littlest JupyterHub: 1–100 users) as well as Kubernetes-scale deployments. It supports external OAuth authenticators. [JupyterHub overview](https://jupyterhub.readthedocs.io/en/latest/), [authentication](https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html)

Marimo is an open-source reactive notebook stored as pure Python. Its deterministic dependency/dataflow model avoids the hidden-state problems that commonly confuse new notebook users. It has built-in package management and can run notebooks as apps or WebAssembly HTML. Marimo documents running its editor inside JupyterHub. [Marimo overview](https://docs.marimo.io/), [deployment](https://docs.marimo.io/guides/deploying/), [WebAssembly notebooks](https://docs.marimo.io/guides/wasm/)

## Marimo re-assessment: strong teaching medium, incomplete classroom platform

The educator material makes Marimo a substantially stronger candidate than the first assessment implied. Its best role is **Marimo notebooks inside JupyterHub**, backed by the separate homework/feedback service described below.

| Course need | Marimo assessment |
| --- | --- |
| Teach data concepts by experimentation | **Excellent.** Reactive execution keeps outputs in sync; sliders, inputs and data widgets make parameter/data changes visible immediately. |
| Reduce environment problems | **Excellent.** `--sandbox` records packages/versions in the notebook and creates an isolated environment, with no learner-maintained requirements file. |
| Give immediate correctness feedback | **Excellent for formative checks.** Test-only cells are discovered and rerun reactively; the same notebook can run under pytest in CI. |
| Teach good notebook habits | **Excellent, with an initial learning cost.** One definition per variable and no hidden state encourage functions and dataflow reasoning. |
| Self-host multi-user class | **Good through JupyterHub, not standalone.** The official JupyterLab extension launches Marimo sessions and supports sandbox/environment selection. |
| Assignment copies, private submission, grades | **Incomplete.** Educator guidance proposes learners fork/download `.py`/`.ipynb`/PDF to submit elsewhere; use Classroom 50, Otter, nbgrader or an LMS. |
| Course-controlled tutor agent | **Partial.** The built-in assistant has read-only and agent modes plus configurable rules, but it is primarily a code-generation assistant, not an assessment/tutor service. |

Marimo's education guidance directly supports follow-along, fill-in-the-blank, structured assignments, lab reports, “tweak and twiddle” exploration, bug hunts, adversarial testing and test-driven learning. For novice data learners, prioritise **tweak-and-twiddle**, guided data replacement, and short bug hunts over fill-in-the-blank coding alone: Marimo explicitly notes that blanks and test-driven exercises are easy to delegate to AI. [Teach with Marimo](https://marimo.io/for-educators), [teaching methods](https://marimo.io/guidelines)

### Recommended Marimo architecture

```text
JupyterHub login → individual workspace → Marimo JupyterLab extension
                  ├─ pinned/sandboxed course notebook + data
                  ├─ local reactive public pytest checks
                  ├─ course-owned @Tutor service (read-only, hint-first)
                  └─ assessed snapshot → Classroom 50/Otter → feedback + Slack
```

Marimo's official JupyterLab extension launches and manages Marimo sessions from JupyterLab, finds available Python environments, and supports sandbox mode; its JupyterHub guide explicitly covers a multi-environment setup. This makes the hybrid practical rather than theoretical. [Marimo on JupyterHub](https://docs.marimo.io/guides/deploying/jupyterhub/)

For public/private *practice* notebooks, molab is compelling: share a GitHub-backed preview link, let learners fork it, and avoid all installation. But its educator FAQ describes homework submission as downloading a file/PDF for another tool, so it should be a zero-ops pilot or practice route, not the authoritative assessed-workflow route. [Marimo educator FAQ](https://marimo.io/for-educators)

### AI policy for a Marimo classroom

Marimo has an unusually capable contextual assistant: it can receive notebook code and explicitly tagged variable values. Its chat modes range from `Manual` (no tools) and `Ask` (read-only inspection) to `Agent` (edit/run cells) and `Code` (powerful kernel manipulation). It can connect to hosted or local models and accepts custom AI rules. That is valuable for exploration but means it must be deliberately constrained in a course. [Marimo AI assistant](https://docs.marimo.io/guides/editor_features/ai_completion/)

- Configure the learner-facing helper as **Manual/Ask** and use the custom rules for the course’s hint-first style; hide generative AI surfaces entirely where an exercise requires unaided work. Do not rely on a rule alone as an integrity control.
- Keep the centrally managed `@Tutor`/homework feedback service as the authoritative pedagogic layer, because it can enforce assignment state, hide tests/solutions, log feedback, escalate to a human and use a course-paid key.
- Reserve Marimo `Agent`/`Code` mode and `marimo pair` for instructor content authoring or clearly labelled advanced practice. `marimo pair` gives an agent full notebook access, including reading variables, running cells and adding/removing cells; it is incompatible with a “help, do not solve” assessment boundary. [marimo pair](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/)

#### Jupyter AI personas vs. Marimo's own AI

**Do not make Jupyter AI the default tutor *inside* a Marimo lesson.** Use Marimo's native assistant for learner-controlled, contextual exploration; keep the course's real `@Tutor` as a separate, course-owned service that receives the submitted Marimo notebook plus test results and returns hint-first feedback. Jupyter AI is a strong option when the course editor is JupyterLab, because it has a documented extension point for custom personas. I found no documented native Jupyter-AI persona integration in the Marimo editor, so in a Marimo workflow it would be an adjacent JupyterLab chat rather than a seamless notebook tutor. [Jupyter AI custom personas](https://jupyter-ai.readthedocs.io/en/stable/developers/index.html)

| Need | Best current choice | Why |
| --- | --- | --- |
| “What does this dataframe/plot mean?” while editing | **Marimo AI, Manual/Ask** | It can use the notebook and explicitly shared values, without granting the default tutor write/run powers. |
| Consistent, course-paid `@Tutor` that gives hints, knows the assignment stage, logs feedback and can alert a human | **External tutor/feedback service** | It is independent of the editor, can be invoked on submission, and can keep private tests, rubric and credentials off the learner machine. |
| Persona in a JupyterLab course | **Jupyter AI** | Its persona mechanism is designed for this use case; use it when JupyterLab is the learner-facing editor. |
| Instructor co-authoring or advanced experimentation | **Marimo Agent/Pair** | Powerful notebook editing and runtime access are useful here, but too much capability for the default novice tutor. |

Marimo does have its own agent path, but it is not yet the course-persona solution to build around: the Agent panel is labelled **experimental**, and its documentation says custom ACP-compatible agents are “coming soon.” Its current external agents (for example, coding-agent CLIs) are best treated as opt-in authoring tools and may request file permissions. Re-evaluate a tightly integrated `@MarimoTutor` when custom agents are stable; until then, a small central service with a read-only submission/test-result contract is lower-risk. [Marimo agents](https://docs.marimo.io/guides/editor_features/agents/), [Marimo Pair](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/)

#### API access versus Codex CLI / Claude Code

Neither environment inherently requires a direct model API key. The distinction is between its **native AI chat** and an **external coding agent**:

| Environment | Use Codex CLI / Claude Code? | Native AI path | Course implication |
| --- | --- | --- | --- |
| **Jupyter AI v3** | **Yes.** It discovers installed Claude Code, Codex CLI, GitHub Copilot CLI and other ACP-compatible agents. The user authenticates the selected agent through its normal CLI login; some agents need an ACP adapter. | Jupyter AI ships with no agent by default; its selected persona supplies the model/agent. | Technically viable, but per-student CLI installation/login is too much friction and introduces individual-account/cost variability for beginners. |
| **Marimo** | **Yes.** `marimo pair` is designed to pair an installed coding-agent CLI with a running notebook; Marimo also has an experimental embedded-agent panel. | Marimo's built-in chat requires a configured provider (OpenAI, Anthropic, Bedrock, Google, GitHub, Ollama, or an OpenAI-compatible endpoint), normally API credentials or a local model. | A good instructor/advanced-user tool, not the default assessment tutor: the agent can obtain broad notebook/runtime access. |

For PyLadies, do **not** require every beginner to install and authenticate Codex CLI or Claude Code. Instead, expose a course-managed `@Tutor` through a backend/proxy with a defined budget and restricted tools. Keep CLI-agent access as an instructor or explicitly opt-in advanced pathway; its precise availability and billing still follow the provider's own CLI account/subscription terms. [Jupyter AI: install agents](https://jupyter-ai.readthedocs.io/en/stable/getting-started.html), [Jupyter AI: notebook tools](https://jupyter-ai.readthedocs.io/en/stable/users/index.html), [Marimo AI providers](https://docs.marimo.io/guides/editor_features/ai_completion/)

### Migration and pilot decision

Convert only new or self-contained lessons first. Existing Jupyter notebooks that depend on order-dependent mutation need restructuring; Marimo will flag conflicts, but a direct conversion is not a free migration. The first pilot should include: (1) an interactive EDA lesson with sliders/filters, (2) a pandas transformation exercise with reactive public tests, and (3) an assessed take-home version run by the external feedback service. Measure learner time-to-first-success, stale-state/support incidents, AI over-help incidents, and tutor review rate against the current Jupyter version.

**Updated recommendation:** retain JupyterHub as the durable multi-user foundation, but promote Marimo from “selective experiment” to the preferred format for new beginner-facing, interactive data lessons—provided private assessment and the tutor remain external services. Marimo is most compelling precisely because it lets a learner alter a working model and instantly see the consequence; that is a better use of AI-era course time than having an agent generate a whole notebook.

Deepnote's cloud project defines the environment (Python, libraries and machine) and provides a project file system; this makes a duplicated assignment a good beginner experience. Its Agent can inspect outputs and create/edit/run blocks. Deepnote documents that its AI is optional and uses external providers under data-protection agreements, but this still requires a deliberate student-data and over-completion policy. It offers dedicated single-tenant/private-VPC arrangements; confirm the available deployment and pricing with Deepnote if self-hosting/data residency is a hard requirement. [Deepnote projects](https://deepnote.com/docs/projects), [notebooks and agent blocks](https://deepnote.com/docs/notebooks), [AI data processing](https://deepnote.com/docs/deepnote-ai), [security/deployment](https://deepnote.com/docs/security-overview)

Deepnote also now has an Apache-2.0 open-source notebook format/toolkit with `.ipynb` conversion and local editor extensions. This is promising for portability, but its own roadmap says that the familiar cloud UI running locally, local agents/BYO keys, and own compute are still upcoming. It is therefore not a replacement for JupyterHub in this course today. [Deepnote Open Source](https://github.com/deepnote/deepnote)

CoCalc is a credible additional option: it combines Jupyter notebooks, real-time collaboration, course management and an AI side chat. It also documents on-prem compute and a self-hosted OnPrem product; factor its commercial licence and a busier all-purpose interface into the evaluation. [CoCalc overview](https://doc.cocalc.com/index.html), [AI Assistant](https://doc.cocalc.com/ai.html), [OnPrem resource model](https://onprem.cocalc.com/ops/resources.html)

## What comparable courses use now

The durable pattern is still **course content in version control + a browser-hosted, prebuilt Jupyter environment**. Berkeley's DataHub explicitly uses JupyterHub so introductory data-science students can begin in a browser on day one rather than set up and maintain an environment. This is strong evidence for retaining JupyterHub as the operational base for a PyLadies course. [Berkeley DataHub curriculum guide](https://curriculum-guide.datahub.berkeley.edu/technology/introduction-to-jupyter/)

The modern additions are collaboration and AI rather than a wholesale replacement of notebooks:

- **Managed classroom products** (Deepnote, CoCalc) remove operations and add live collaboration, comments and easy duplication of a prepared environment. Choose them where teaching-team capacity is scarcer than vendor dependence.
- **Reproducible content repositories** remain important: for example, the Hugging Face course keeps source content in Git and generates Jupyter notebooks from it. This is a useful model even if learners run the notebooks in a hosted environment. [Hugging Face course workflow](https://github.com/huggingface/course/blob/main/README.md)
- **AI-native notebooks** now let an agent inspect context and execute work. That makes them powerful, but a default coding agent optimises task completion, not learning. A tutor must be deliberately constrained and evaluated, not merely enabled.

For this course, trial Deepnote alongside the JupyterHub proof of concept only if a managed SaaS option is acceptable. Test the same exercise as an individual copy, a pair-programming task and a submitted assignment. Compare setup friction, collaboration, export/portability, cost, and whether the available AI can be made hint-first. Do not make an AI vendor's generic agent the sole learning-support strategy.

## Home assignments, collection and feedback

Use a single **source-of-truth assignment repository**, generate a learner copy with solutions/hidden tests removed, and submit an immutable snapshot at the deadline. Learners should retain their working copy; graders and the tutor must work from the snapshot, assignment version and pinned grading image. This prevents a later edit from changing what was assessed.

| Need | JupyterHub route | Managed-platform route |
| --- | --- | --- |
| Distribute/collect | **nbgrader** release/collect exchange | Deepnote private project per learner, or LMS/Git repository upload |
| Deterministic code checks | **nbgrader** hidden/public tests in a fixed image | **Otter-Grader** package/container run after upload; it also produces a Gradescope autograder bundle |
| Open-ended analysis and writing | Human rubric review after test results | Human rubric review and comments |
| Return feedback | nbgrader HTML feedback or course/LMS feedback | Deepnote comments/link/PDF, or LMS feedback |

`nbgrader` is the direct JupyterHub choice: it supports release, collection, hidden/read-only tests, bulk autograding, manual points/comments in Formgrader, a gradebook, and generated HTML feedback. Its structured workflow is worth the setup cost if the course owns the Hub. [nbgrader workflow](https://nbgrader.readthedocs.io/en/stable/user_guide/creating_and_grading_assignments.html), [nbgrader feedback/gradebook](https://nbgrader.readthedocs.io/en/stable/user_guide/what_is_nbgrader.html)

**Otter-Grader** is the more portable choice when submission is through an LMS, GitHub Classroom, or a future platform change. It generates a sanitized learner notebook and a separate autograder package containing tests/solutions; it can grade locally in containers or through Gradescope and emits a grades CSV. Berkeley uses it in DataHub support. [Otter workflow](https://otter-grader.readthedocs.io/en/latest/tutorial.html), [test visibility](https://otter-grader.readthedocs.io/en/master/workflow/executing_submissions/gradescope.html), [Berkeley DataHub](https://curriculum-guide.datahub.berkeley.edu/support/troubleshooting/otter-grader)

Deepnote is adequate for low-volume homework distribution, private individual projects, progress inspection and comments, but its own education docs say it has **no integrated autograding solution** and that listed packages do not comprehensively handle hundreds of submissions. Do not select Deepnote for its grading automation. [individual assignments](https://deepnote.com/docs/individual-assignments), [autograding limitation](https://deepnote.com/docs/auto-grading-solutions)

### Recommended grading design

For each home task, declare the learning objectives, allowed AI use, deadline/resubmission rule, rubric and a known package image. Use two evidence streams:

- **Automatic, objective checks**: imports, function contracts, output shape/types, invariants, edge cases, absence of warnings, and a clean “restart and run all.” Show small public checks during work; keep robustness checks hidden until submission.
- **Human-reviewed rubric**: question framing, data-cleaning rationale, visualisation/readability, interpretation/limitations, and short reflection (“what did I try; what did I change after feedback?”). Tests cannot credibly score these.

An initial split such as 50% tests, 35% analysis/communication rubric, 10% reproducibility, 5% reflection is a useful starting point. Calibrate the rubric by having two instructors/mentors independently mark a small sample before publishing grades. Publish exemplar *reasoning* after the deadline, rather than only a final notebook.

Run submitted notebooks in a disposable, network-restricted container with CPU/RAM/time limits and no course secrets. Never execute a learner notebook in the instructor/Hub control environment. Keep hidden tests out of the learner image; accepting that tests detect correctness, not authorship. Any academic-integrity decision needs human review and a chance for the learner to explain their work.

### `@HomeworkTutor`: feedback without doing the homework

Give the tutor a separate submission-feedback mode. It receives only the assignment prompt/version, approved rubric, learner snapshot, execution/test summary, and any explicitly shared context—not hidden tests, solutions, other learners' work, or grading credentials.

| Moment | Tutor behaviour |
| --- | --- |
| Before submission | Run/interpret public checks; ask a diagnostic question; give one hint and a smallest-next-step. Do not provide a completed cell or solution. |
| After a failed check | Explain the symptom, identify the relevant concept, propose one experiment, and ask the learner to retry. It must not reveal hidden-test inputs or expected outputs. |
| On submission | Produce a private **feedback draft**, structured as strengths, 1–3 priority improvements, rubric evidence, and a revision plan. It may assign “needs human review,” never a final course grade. |
| After grading | Explain the released human/test feedback and help make a revision. Release official solution/exemplar only according to the course policy. |

The tutor's response should cite notebook cells/output and rubric criteria, distinguish observed facts from inference, and state when it cannot assess an open-ended claim. Log the exact prompt, model/version, sources and response with the feedback draft; provide an “incorrect/unhelpful” report button. These logs support appeal, calibration and prompt improvement without turning surveillance into a course feature.

AI feedback can be useful for a second perspective and for drafting detailed rubric-grounded comments, but not as the sole assessment decision-maker: OpenAI's assessment guidance explicitly requires a human in the loop because models can be biased or inaccurate. Treat the instructor/TA as final grader; use the agent to triage failures, draft comments and aggregate **de-identified** misconceptions for the next lesson. [Assessment and feedback guidance](https://help.openai.com/en/articles/8313397-how-can-chatgpt-be-used-for-assessment-and-feedback), [rubric feedback-helper pattern](https://academy.openai.com/en/public/clubs/higher-education-05x4z/blogs/built-for-better-teaching-5-gpts-every-faculty-member-should-use-2025-08-13)

### Instant feedback and Slack integration

Yes—this is feasible with nbgrader, but it needs a small integration service. The normal nbgrader filesystem exchange writes timestamped submissions into an `inbound` area and `collect` imports the newest one; its documentation does not describe an outbound “new submission” webhook. nbgrader does expose an Exchange API and a high-level Python API for collection/autograding, so a course can add this event layer without forking the grader. [filesystem exchange](https://nbgrader.readthedocs.io/en/latest/user_guide/what_is_nbgrader.html), [Exchange API](https://nbgrader.readthedocs.io/en/latest/exchange/exchange_api.html), [high-level API](https://nbgrader.readthedocs.io/en/latest/api/high_level_api.html)

```text
Submit in JupyterHub
        │ immutable timestamped snapshot
        ▼
submission listener → durable queue → sandboxed nbgrader/Otter run
                                        │ tests + notebook evidence
                                        ▼
                              @HomeworkTutor feedback draft
                                │                    │
                   feedback folder/UI link       Slack DM: “ready”
                                │                    │
                         learner revises      human-review queue
```

**Implementation choices.** The cleanest option is a custom `ExchangeSubmit` implementation that writes the snapshot and enqueues a job only after the write succeeds. A lower-effort pilot is a privileged, read-only watcher of the exchange `inbound` directory which validates a completed timestamped directory and enqueues it. Do not trigger directly from an arbitrary file-change event: wait for a complete/validated snapshot and deduplicate on `(student, assignment, timestamp, content hash)`. A worker then runs the normal `collect`/`autograde` path in a disposable container, stores a structured result, invokes the tutor, and releases a preliminary feedback HTML/Markdown file through the normal nbgrader feedback exchange. nbgrader's feedback mechanism already supports feedback per submission timestamp, and its feedback generator has pre/post conversion hooks; those are useful for the **release** step but are not a substitute for a submission event. [collection semantics](https://nbgrader.readthedocs.io/en/latest/command_line_tools/nbgrader-collect.html), [feedback hooks](https://nbgrader.readthedocs.io/en/stable/command_line_tools/nbgrader-generate-feedback.html)

Make this a JupyterHub Service called, for example, `homework-feedback`, with only the scopes it needs. JupyterHub supports managed or external services, service API tokens and OAuth-authenticated service pages; do not give this service blanket admin access or a token capable of reading every live learner server. [JupyterHub Services](https://jupyterhub.readthedocs.io/en/latest/reference/services.html)

**Slack should be a notification and human-handoff surface, not the place where submissions live.** Use a proper Slack app rather than a bare webhook:

- Send a private DM such as “Preliminary feedback for HW03 is ready” with a link back to the authenticated JupyterHub feedback page. Never put notebook contents, scores, hidden-test details or personal data in a public channel.
- Give each learner an opt-in private `#help-hw03` thread or direct bot conversation. `Request human review` creates a minimal ticket with the submission ID, rubric/test summary and learner’s question; a tutor claims it and continues in a private thread.
- Give staff a private `#course-tutors` queue containing only review flags (learner request, low model confidence, sandbox failure, possible grading discrepancy). Aggregate anonymised misconception counts for the whole channel; link staff to the authenticated review page for the actual work.
- Use Slack Events API and `chat.postMessage`/interactive actions for a conversational bot and review buttons. Incoming webhooks are sufficient only for fixed-channel announcements and do not return the message timestamp needed for easy threaded replies. [Slack Events API](https://api.slack.com/apis/connections/events-api), [incoming webhooks and threads](https://api.slack.com/messaging/webhooks)

The student’s DM must be mapped to their Hub identity during an explicit OAuth/linking step. Enforce object-level access: a learner can retrieve only their own feedback; a tutor sees only tickets assigned to them. Keep the LLM call and feedback record on the course service, not in Slack logs; expire Slack notifications and audit records according to the cohort privacy policy.

Suggested states are `queued → tests-running → preliminary-feedback-ready → learner-revised | review-requested → human-reviewed → released`. “Preliminary” deliberately means formative and revisable; official score and grade release occur only after the agreed human/automatic grading process. Start with a 10-learner pilot and measure median feedback latency, false/unsafe feedback reports, human-review rate, and tutor time saved.

### Is Otter better for the AI-feedback integration?

**Usually yes for the feedback service; not automatically for the whole course.** Otter generates a sanitized learner notebook plus a separate autograder bundle, runs submissions in containers (or Gradescope), and emits a score breakdown/CSV. That makes the integration boundary especially clean: the listener hands one immutable submission and one versioned autograder image to a worker; the worker returns a structured test result for `@HomeworkTutor`. The same worker can run outside JupyterHub and later accept submissions from an LMS or GitHub Classroom. [Otter workflow](https://otter-grader.readthedocs.io/en/latest/tutorial.html)

Choose **Otter + a small submission/feedback service** if portability, isolated execution, asynchronous jobs and future platform flexibility matter most. Choose **nbgrader + the same service** if JupyterHub-native release/collect, Formgrader, a shared gradebook and HTML feedback are more valuable than a cleaner boundary. In either case the tutor design is identical: give it the learner snapshot, rubric and *sanitised test summary*, never the solution or hidden tests.

For PyLadies, a sensible sequence is: use nbgrader for the first JupyterHub pilot (less course-management plumbing), but define the feedback worker's input/output as platform-neutral from day one. Trial Otter for the first assignment that has substantial hidden tests or needs a container image. If it proves easier to operate, migrate distribution/collection later without rewriting `@HomeworkTutor` or the Slack handoff.

### Classroom 50: a strong GitHub-based homework layer

[Classroom 50](https://github.com/foundation50/classroom50/) is a credible fourth option for **homework management**, not a replacement for the notebook environment. It is a free, open-source GitHub Classroom alternative: a static web app/CLI with no application server or database of its own; classroom state, repositories, permissions, submission history and grades live in a GitHub organisation. Current docs say it supports individual/group work, autograding, inline feedback, roster/submission/score tracking, and requires a GitHub Team or Enterprise organisation (GitHub Education may cover verified teachers). [Classroom 50 overview](https://github.com/foundation50/classroom50/wiki)

It is unusually well-suited to the immediate-feedback pipeline. Each push to a learner's `main` branch triggers GitHub Actions, produces an immutable `submit/<timestamp>-<sha>` tag, and publishes a GitHub Release containing a versioned `result.json` with score, test breakdown, commit and review links. Tests can be declarative, pytest-based, or a custom `autograder.py`, so an Otter notebook grader can be wrapped inside it. [Classroom 50 autograder architecture](https://github.com/foundation50/classroom50/wiki/Autograders)

```text
learner commits/pushes → Classroom 50 GitHub Action → result.json + Release
                                                        │ GitHub App webhook
                                                        ▼
                                        @HomeworkTutor / human-review service
                                                        ├─ GitHub feedback/check
                                                        └─ private Slack DM + tutor queue
```

Use a dedicated GitHub App, subscribed to `release` or completed `workflow_run` events, to send the release ID to the feedback service queue. The service then reads the known commit and `result.json`, invokes the tutor with the rubric and sanitised result, and writes feedback through a minimally privileged GitHub API client. GitHub Apps provide real-time webhooks for exactly this pattern. [GitHub App webhooks](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/using-webhooks-with-github-apps), [workflow-run events](https://docs.github.com/en/webhooks/webhook-events-and-payloads?actiontype=released)

Do **not** put model-provider or Slack secrets into each learner repository's Action: learners can change code and workflows. Keep secrets and the LLM call in the central feedback service/GitHub App, verify webhook signatures, and fetch only the final tagged commit. GitHub's security guidance similarly treats untrusted workflow code/secrets as a critical boundary. [GitHub Actions security guidance](https://docs.github.com/en/enterprise-server%403.17/actions/reference/security/securely-using-pull_request_target)

**Fit for PyLadies:** use it if Git/GitHub collaboration is an explicit course objective and participants can manage GitHub accounts. It gives a cleaner event and evidence trail than nbgrader and is likely the best route for the Slack/AI handoff. Do not make it the primary beginner workspace: the learner still needs a separate execution environment (JupyterHub/Deepnote/local), and repositories, commits and GitHub permissions add cognitive load. A practical hybrid is **JupyterHub or Deepnote for lessons; Classroom 50 + Otter/pytest for assessed take-home work; one central `@HomeworkTutor` service for feedback and Slack escalation**.

## Proposed classroom shape

```text
participant browser → JupyterHub login → isolated JupyterLab workspace
                                      ├─ course image: Python + pandas + sklearn + lessons/data
                                      ├─ Jupyter AI: @Tutor persona
                                      └─ optional Marimo editor for reactive lessons
```

Start with one small VM and a prebuilt, version-pinned course image. Require no participant installation. Persist each home directory; reset/rebuild only the shared image between cohorts. Add idle shutdown, CPU/RAM limits, backups, HTTPS, and an OAuth allow-list. Do not use a shared-password deployment for a real course with personal work.

For a genuine local/offline fallback, distribute the same locked environment in a one-command launcher or container only to participants who want it. There is no zero-maintenance local Python stack: browser-first is the seamless default.

## Tutor agent: make it teach, not solve

Jupyter AI now treats agents as selectable chat personas and supports adding custom personas through Python package entry points; agents can use the Jupyter MCP server, with permission prompts for actions beyond workspace reads. [Jupyter AI getting started](https://jupyter-ai.readthedocs.io/en/stable/getting-started.html), [custom persona developer API](https://jupyter-ai.readthedocs.io/en/stable/developers/index.html)

Implement `@Tutor` with a course prompt and retrieval over the current lesson, glossary, expected concepts, and common errors. Its policy should:

- ask one diagnostic question and offer a hint ladder before showing a solution;
- explain tracebacks in Czech/English-friendly plain language and inspect only the current selected cell/notebook;
- refuse to write the final exercise answer until the learner has attempted a step; offer a minimal example on unrelated toy data instead;
- cite the relevant lesson section, identify uncertainty, and invite escalation to a human coach;
- default to **read-only** tools. Keep file writes, shell commands, network access, package installation, and notebook execution off or explicitly approved.

Use a centrally managed model/API proxy so learners neither configure keys nor see a shared secret. Apply per-user/course spending limits and logging minimised for privacy. Treat uploaded datasets and notebook content as data sent to the chosen model provider unless using a local/private model; Jupyter AI explicitly flags this third-party-data consideration in its user guidance.

Useful companion personas: `@Debugger` (error explanation + smallest next experiment), `@DataCoach` (questions about assumptions, missing data, leakage and visualisation), and `@Reviewer` (rubric-based feedback without code completion). The teaching team should be able to change their instructions and knowledge independently of the notebook image.

## A short proof of concept

1. Deploy 10–20 JupyterHub accounts with the existing `pandas` lesson, pinned dependencies, one sample dataset, and Jupyter AI's read-only `@Tutor`.
2. Convert one self-contained lesson to Marimo and compare: time-to-first-cell, environment/support requests, completion rate, and whether reactivity helps or confuses beginners.
3. Review a small anonymised sample of tutor chats against a rubric: did it diagnose, hint, explain, and preserve learner agency? Track cost and unsafe/over-helpful responses.

Choose Marimo more broadly only if the pilot shows that its reactive model improves learning without making the course's existing Jupyter ecosystem harder to use. Keep JupyterHub as the durable multi-user foundation either way.
