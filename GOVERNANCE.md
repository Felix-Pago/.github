# Felix-Pago Project Governance

This document outlines how the Felix-Pago organization is managed and how decisions are made regarding our technical stack and infrastructure.

## 👥 Roles & Responsibilities

### 1. Contributors
Anyone who submits code, documentation, or issues. 
* **Responsibility**: Follow the `CONTRIBUTING.md` guidelines and maintain high code quality.

### 2. Maintainers (Core Team)
Developers with write access to repositories.
* **Responsibility**: Review Pull Requests, manage issues, and ensure CI/CD pipelines (ci-gate-check) are passing.
* **Authority**: Can approve and merge PRs into `main`.

### 3. Administrators
The engineering leadership team.
* **Responsibility**: Manage organization settings, secrets, and repository permissions.
* **Authority**: Final say on architectural shifts and security policy overrides.

## ⚖️ Decision-Making Process

We aim for **consensus-based** decision-making. 

1. **Proposals**: Significant changes (new frameworks, architectural shifts) should start as an Issue or an RFC (Request for Comments).
2. **Review**: Maintainers have 3 business days to provide feedback on major proposals.
3. **Resolution**: If consensus is not reached, the Administrators will make the final decision based on security, scalability, and business priority.

## 🔐 Security & Compliance
All repositories must adhere to the Felix-Pago security baseline:
* **Mandatory Reviews**: At least one Maintainer must approve a PR before merging.
* **Branch Protection**: Force pushes to `main` are disabled.
* **Automated Scanning**: IaC scans (Checkov) must pass for all infrastructure changes.

## 📞 Escalations
For urgent security issues or governance disputes, please contact the administrators directly or email `security@felixpago.com`.

---
*Last Updated: February 2026*