---
description: First-run setup for the GMMSB toolkit — SSH key, plugin wire-up, machine check.
---

Run `gmmsb init-agent` and walk the user through the output.

1. Execute `gmmsb init-agent` via the Bash tool.
2. Read the "ssh check" table. For every row where the status is **auth needed**,
   surface the `ssh-copy-id …` command and tell the user to run it themselves
   (it needs their password). Do **not** try to run it yourself.
3. Once the user reports back that they've run the commands, run
   `gmmsb init-agent` again to re-verify.
4. For any machine where the user doesn't have an account, ask:
   - "Do you log into `<machine>` with a different username?" → if yes,
     suggest `gmmsb machine override <name> --user <name>` and tell them
     to re-run `gmmsb init-agent`.
   - "No account at all?" → offer to draft a message to the sysadmin
     asking for an account.
5. When all machines are green, tell the user they can now ask you to run
   tools — e.g. "list registered tools" or "run noop on workstation-01".

Do not edit `~/.config/gmmsb/machines.yaml` yourself unless the user
explicitly asks for it.
