# Enterprise Governance for Copilot Cost Control

[English](12-enterprise-governance.md) | [繁體中文（台灣）](12-enterprise-governance.zh-TW.md)

[← Back to Guide](index.en.md)

---

This page is for org and enterprise admins. Goal: control spend without inventing controls GitHub does not document.

## What Actually Controls Spend

Three levers matter most:

1. budget ceilings
2. user-level budget control
3. model availability

Prompt compression still matters, but it is a usage-efficiency lever. It is not an admin billing control.

One timing rule matters: June 1, 2026 is the cutoff. After that, Business and Enterprise governance shifts to AI-credit usage under usage-based billing. Treat premium requests as legacy transition context, not as the main planning model.

## 1. Set Budgets First

Use GitHub's [usage-based billing guidance for organizations and enterprises](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises) and [metered product budget setup docs](https://docs.github.com/en/billing/how-tos/budgets/setting-up-budgets-to-control-spending-on-metered-products).

Key points from GitHub docs for Business and Enterprise after June 1:

- budgets can be set at organization, enterprise, or cost-center scope
- you can enable stop usage when budget is reached
- user-level budgets exist, and a **$0** user budget means no access to usage-based features

That budget system is the direct spend cap for AI-credit usage at enterprise, organization, cost-center, and user scope.

Important caveat: budgets do **not** make prompts smaller. They do **not** reduce tokens per prompt. They cap AI-credit spend.

Practical default:

1. set a nonzero test budget for rollout
2. enable alerts early
3. enable stop usage once reporting looks sane
4. review monthly, not just after overruns

## 2. Use User-Level Budgets for Per-User Tightening

For Business and Enterprise after June 1, the clean per-user cap is the **user-level AI credit budget** documented in GitHub's [usage-based billing guidance](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises). GitHub's docs explicitly say a user-level budget of **$0** means that user gets no access to usage-based features.

Admin mindset: think in AI-credit usage first. Model choice, chat depth, agent duration, and user-level budget are now direct spend controls.

Do **not** claim a documented org-level per-user model toggle for Copilot Chat in IDEs. GitHub's docs describe budgets, cost centers, and allowance management. They also document org and enterprise model access policy at the member level, but not a within-one-org per-user model matrix you can arbitrarily tune model-by-model.

Practical pattern:

1. baseline group gets a low user-level AI-credit budget
2. power users get more only with clear job need
3. monthly review: downgrade users whose usage does not justify the extra cost

Post-June 1 admin tips:

1. watch long chat and agent sessions because repeated turns now accumulate AI-credit cost directly
2. monitor user-level budgets closely because **$0** removes access to usage-based features
3. remember code completions and next edit suggestions are not billed in AI credits, so do not treat all Copilot activity as equal cost
4. review model choice regularly because chat-style interactions now consume AI credits based on model and tokens
5. keep terse repo instructions in IDE workflows because lower output volume still reduces AI-credit burn even when billing moves off request counts

Legacy note: if you are still preparing customers before June 1, [premium request management](https://docs.github.com/en/copilot/concepts/billing/premium-request-management) explains the outgoing control model. Use that only as transition guidance.

## 3. Review Models Before You Enable Them

Use [Configuring access to AI models in Copilot](https://docs.github.com/en/copilot/using-github-copilot/ai-models/configuring-access-to-ai-models-in-copilot).

GitHub documents that organization owners and enterprise owners can enable or disable access to AI models for members. Treat that as the supported model-governance control.

That is not the same thing as finely tuned per-user model toggles inside one org. For different org-level model policies or separate billing boundaries, separate organizations can still be useful. Use that only when the boundary is worth the overhead.

Practical review checklist:

1. which workflows actually need premium models
2. which teams produce measurable value from them
3. which users can stay on Auto or included models
4. what usage report you will inspect after enablement
5. what rollback rule you will use if spend jumps without quality gain

Bad rollout pattern: enable every premium model for the whole org because a small group asked for one hard task.

Better rollout pattern: approve model access in stages, then compare usage and output quality before widening.

## 4. Keep Custom Instructions in the Right Scope

GitHub documents repository instructions for IDEs and GitHub.com in [Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) and the IDE-specific companion page linked there.

GitHub documents organization instructions in [Adding organization custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-organization-instructions).

Important scope rule from GitHub docs:

- repository custom instructions are valid repo-level guidance
- organization custom instructions are currently supported for Copilot Chat on GitHub.com, Copilot code review on GitHub.com, and Copilot cloud agent on GitHub.com
- do **not** assume organization instructions apply in IDEs

That last point matters for cost control. If you want terse behavior in VS Code or JetBrains, put the always-on guidance in repository instructions, not only in org instructions.

Practical split:

- org instructions: broad policy tone, review reminders, cross-repo defaults for GitHub.com surfaces
- repo instructions: concrete coding, build, and terseness rules that must apply in IDE workflows
- path-specific instructions: narrow local rules where extra context pays for itself

## 5. Separate Orgs Can Work, but Treat It as a Caveated Workaround

GitHub's model-access and billing controls make separate organizations a possible way to maintain different org-level model policies or billing boundaries.

This can be useful when you need different org-level model policies or distinct billing boundaries for different user populations and your current org structure already matches those groups.

But this is a caveated workaround, not a magic governance feature.

Tradeoffs:

- more admin overhead
- license-assignment complexity
- awkward fit if users span many orgs
- SCIM and cost-center structure may drive the answer more than Copilot alone

Use separate orgs only when the policy or billing boundary is worth the operational cost. It is a fallback, not the first choice.

## 6. Measure the Right Thing

Use GitHub usage reports and AI-credit reporting from the billing docs above. Ask four questions:

1. which teams exceed baseline spend most often
2. which users drive the most AI-credit usage
3. which models correlate with better outcomes vs simple habit
4. which agent workflows create large spend without commensurate delivery value

Supplemental benchmarking can help when comparing model quality and price posture. [llm-stats.com](https://llm-stats.com/) is useful as an independent reference point. Treat it as supplemental benchmarking, **not** official GitHub guidance and **not** a substitute for your own Copilot usage reports.

## 7. June 1 Cutover Checklist

If you are preparing customers for the June 1 shift, do this first:

1. move admin guidance from request counters to AI-credit budgets
2. decide which users need tight user-level budgets and which teams can share a broader pooled budget
3. review model availability before frontier models become direct AI-credit spend
4. remind teams that code completions and next edit suggestions stay outside AI-credit billing
5. watch long chat and agent workflows first because they become the fastest spend amplifiers

## Recommended Enterprise Default

1. use Auto as the default model path
2. set budgets before broad rollout
3. use user-level AI credit budgets when you need tighter per-user control
4. review premium models before enablement
5. keep repo instructions small so IDE workflows inherit the right defaults
6. use separate org segmentation only if cost-center boundaries already support it

This is boring on purpose. Cheap defaults first. Premium access by exception. Measurement before expansion.
