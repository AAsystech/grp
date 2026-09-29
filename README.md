# GRP

GRP is an AI-powered public service platform designed to help citizens submit, manage, and track service requests through web, mobile, voice, and conversational interfaces.

## Repository Structure

    apps/
    ├── backend/         FastAPI + LangGraph multi-agent backend
    ├── citizen-web/     Citizen web application
    ├── agent-console/   Internal AI agent interface
    └── mobile/          Flutter mobile application

    packages/            Shared packages and contracts
    infrastructure/      Infrastructure as Code
    docs/                Architecture and project documentation
    scripts/             Development and operational scripts
    .github/workflows/   CI/CD workflows

## Backend

The GRP backend is designed around:

- FastAPI
- LangGraph
- Multi-agent workflows
- PostgreSQL (Neon)
- Docker

Individual agents can contain their own workflows/subgraphs while participating in the overall GRP orchestration.

## Deployment

The planned deployment architecture uses:

- Docker
- Google Artifact Registry
- Google Cloud Run
- GitHub Actions
- Terraform
- Neon PostgreSQL

## Applications

### Backend

    apps/backend

FastAPI backend containing the LangGraph agent platform, APIs, tools, services, and database integrations.

### Citizen Web

    apps/citizen-web

Web interface used by citizens to access GRP services.

### Agent Console

    apps/agent-console

Internal interface for developers and authorized users to interact with GRP agents.

### Mobile

    apps/mobile

Flutter application for Android and iOS.

## Development

Each application contains its own development and setup documentation.