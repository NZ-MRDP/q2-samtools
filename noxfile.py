"""Nox sessions for q2-samtools development tasks."""

import nox

# nox.options.sessions = ["test", "lint", "coverage", "typing"]
nox.options.sessions = ["lint", "typing"]


@nox.session(python=["3.10"])
def test(session):
    """Run the test suite."""
    session.run("uv", "sync", "--group", "dev", external=True)
    session.run("uv", "run", "pytest", external=True)


@nox.session
def coverage(session):
    """Run tests with coverage enabled."""
    session.run("uv", "sync", "--group", "dev", external=True)
    session.run("uv", "run", "pytest", "--cov=q2_samtools", "--cov-report=term-missing", external=True)


@nox.session
def lint(session):
    """Run Ruff checks."""
    session.run("uv", "sync", "--group", "dev", external=True)
    session.run("uv", "run", "ruff", "check", ".", external=True)


@nox.session
def typing(session):
    """Run Pyright type checking."""
    session.run("uv", "sync", "--group", "dev", external=True)
    session.run("uv", "run", "pyright", ".", external=True)
