# praxis

**praxis** is my personal Python utility library.

It contains functions and small tools that I use in my day-to-day work: research, scripting, data handling, and general computational tasks that recur often enough to justify being written once and reused deliberately.

This library is not designed for a general audience. Others are free to use it, but they are not its intended users.

---

## Intent

I created `praxis` to avoid rewriting the same code across projects and to keep a disciplined, readable, and reusable core of utilities that reflect how I actually work.

Only functions that meet the following criteria are included:

- I use them repeatedly in real projects
- They solve a concrete and recurring problem
- Their behavior is explicit and easy to reason about
- They can be understood by reading the code alone

If a function does not satisfy these conditions, it does not belong here.

---

## Installation

### From GitHub

```bash
pip install git+https://github.com/sigifredo/praxis-py.git
```

## What This Library Is Not

- A general-purpose utility package
- A framework
- A showcase project
- A stable public API

Changes may be made whenever they are useful to me, without regard for backward compatibility.
