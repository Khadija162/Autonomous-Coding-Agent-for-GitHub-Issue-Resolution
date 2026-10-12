# Architecture and implementation boundary

**Committed prototype:** FastAPI analysis backend, Streamlit frontend, read-only source search, tree-sitter Python parsing, read-only public GitHub issue adapter (standalone), opt-in Ollama coding model with mock default, local evaluation record writer, fixed-command sandbox helper for trusted fixture code, original CC0 issue dataset, CI, Docker Compose and Azure storage Terraform.

**Not implemented:** automatic patch writing, iterative repair, unattended test execution from the web, branch creation, real GitHub PR publication, production runner isolation, Azure Container Apps, PostgreSQL operational metrics or hosted LLM inference.

**Future data engineering:** ingest public GitHub issue metadata under approved terms -> lineage-aware issue store -> code symbol indexes -> retrieval metrics -> agent trace/event records in PostgreSQL or Parquet -> SWE-bench pass rates and regressions. Never commit private repository content to a public index.

**Cloud blueprint:** Azure Container Apps for authenticated dashboard/API, queue-based job scheduling, disposable isolated worker VMs/AKS jobs for untrusted code, ADLS Gen2 for artifacts, Azure Database for PostgreSQL, Key Vault, managed identities and Azure Monitor. Model host on dedicated GPU compute via vLLM or Ollama. Infrastructure here only declares a resource group and storage account; nothing is deployed.

**Security:** issue text and source are untrusted; restrict GitHub credentials to least privilege, require human approval before writes/PR, run untrusted tests in disposable VMs with no outbound network, avoid mounting Docker socket and don't publish an unauthenticated API.
