# Project rules
- Project: GraphRAG Financial Research Copilot (multi-tenant, team-aware RAG over company filings).
- Language: Python 3.12, FastAPI (async), SQLAlchemy 2 + Alembic, Pydantic v2, uv for dependencies.
- Stores: Qdrant (vectors), Neo4j (graph), PostgreSQL (metadata, RBAC, chat, evals, financial tables), Redis (cache, rate limit).
- Clouds: Azure = identity, governance, app hosting (Entra ID, resource groups, RBAC, Container Apps, Key Vault, PostgreSQL Flexible Server, ACR, App Insights). AWS = data and ML plane (S3, SQS, Lambda ingestion trigger, SageMaker forecasting endpoint).
- IaC: Terraform only (providers: azurerm, azuread, aws). No click-ops.
- Every feature needs: type hints, a pytest test, and a line in docs/.
- Never hardcode secrets. Local = .env; cloud = Azure Key Vault.
- Local dev must work with `docker compose up` without any cloud account (use MinIO for S3, LocalStack for SQS, a mock auth provider flag AUTH_MODE=dev).
- Commit style: conventional commits. Run `make lint test` before declaring a phase done.
- Authorization rule: EVERY query to Postgres, Qdrant and Neo4j must be filtered by the caller's allowed team_ids. Never return data without that filter.
TARGET ARCHITECTURE
User -> Entra ID (OIDC login, groups claim) -> FastAPI (Azure Container Apps)
   FastAPI -> Router agent (LangGraph) -> { Qdrant hybrid search | Neo4j Cypher | Postgres text-to-SQL | SageMaker forecast tool }
   FastAPI -> Postgres (RBAC, chat, metadata)   Redis (cache, rate limit)

Upload PDF -> S3 (AWS) -> SQS -> Lambda -> HTTPS call to ingestion worker (Container Apps job)
   worker: parse -> chunk -> embed -> Qdrant + Neo4j + Postgres (all tagged with team_id)

Observability: Azure Application Insights + Prometheus/Grafana + Langfuse (LLM tracing)
Eval: RAGAS golden set in CI, MLflow tracking, fail build if metrics drop
Azure governance model (the part to showcase)

Resource groups (one per environment and concern):

Resource group	Contains
rg-grc-dev-app	Container Apps env, ACR, App Insights, Log Analytics
rg-grc-dev-data	PostgreSQL Flexible Server, Redis, Storage
rg-grc-dev-sec	Key Vault, managed identities
rg-grc-prod-*	Same three, for prod
rg-grc-shared-tfstate	Terraform remote state storage account

Entra ID groups (created with the azuread provider):

Group	Purpose	Azure RBAC role	App role
grc-platform-admins	Platform owners	Owner on dev rgs, Contributor on prod	admin
grc-engineers	Developers	Contributor on dev rgs, Reader on prod	engineer
grc-analyst-research	Team: Research	Reader	analyst (team Research)
grc-analyst-risk	Team: Risk	Reader	analyst (team Risk)
grc-viewers	Read-only business users	Reader	viewer

Key Vault access uses RBAC (not access policies): app managed identity gets Key Vault Secrets User; grc-platform-admins get Key Vault Administrator.

App-level model: Entra group (object ID) -> teams row -> memberships -> document visibility. Group object IDs arrive in the token groups claim and are mapped to teams at login.
