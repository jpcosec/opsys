"""End-to-end suite where a cheap agent (pi + DeepSeek Flash) uses deskops from its docs alone.

Two questions, answered separately:

1. Does everything that has to work, work? Each scenario carries a reference solution;
   `test_reference_solutions` runs setup, reference and checks with no LLM, in the normal suite.
2. Are the docs good enough? `test_agent_scenarios` (opt-in, `DESKOPS_AGENT_E2E=1`) hands the
   scenario's docs and intent to an agent in a sandbox. The harness, not the agent, judges the
   outcome with the same checks, and measures how the agent got there: failed commands, `--help`
   probing, reads of deskops/sldb source (the docs were not enough), and the friction it reports.

See tests/e2e_agent/README.md.
"""
