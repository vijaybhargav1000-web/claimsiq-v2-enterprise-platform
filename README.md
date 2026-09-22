# ClaimsIQ — Intelligent Claims Data & Decisioning Platform

## Overview

ClaimsIQ is an enterprise-style intelligent claims data and decisioning platform built on **Amazon Web Services (AWS)** using **Terraform and Infrastructure as Code (IaC)**.

The project brings together cloud infrastructure, data engineering, Generative AI, Retrieval-Augmented Generation (RAG), and intelligent claims decisioning into a single end-to-end platform.

The goal is to demonstrate how a traditional claims processing environment can be transformed into a modern, scalable platform that can ingest and organize claims data, retrieve relevant business knowledge, assist users with AI-generated insights, and support claims triage and decision-making.

The platform combines:

- **AWS cloud infrastructure** for networking, compute, storage, security, and monitoring
- **Terraform** for repeatable and modular infrastructure provisioning
- **S3-based data lake architecture** using Bronze, Silver, and Gold layers
- **RAG and Generative AI** for retrieving relevant claims and policy knowledge
- **OpenSearch-based retrieval** for semantic search and grounded context
- **Agentic decisioning patterns** for claim triage, risk evaluation, escalation, and manual review
- **FastAPI and Streamlit** for the application and user-facing experience
- **Docker and GitHub Actions** for reproducible application delivery and CI/CD
- **Auditability and observability** to support production-oriented troubleshooting and traceability

The architecture is designed with a clear separation between **data processing, AI retrieval, business decisioning, and infrastructure**, allowing each layer to evolve independently while still working together as one enterprise platform.

## Key Features

### ☁️ AWS & Infrastructure

- Modular Infrastructure as Code using Terraform
- Secure VPC architecture with public and private subnets
- Application Load Balancer with target groups
- EC2-based compute with Auto Scaling
- IAM and Security Group controls
- Amazon S3 for enterprise data and application storage
- Amazon RDS for relational workloads
- Amazon CloudWatch for monitoring and observability

### 🗄️ Data Engineering & Analytics

- Multi-layer S3 Data Lake architecture using Bronze, Silver, and Gold layers
- Batch and streaming ingestion patterns
- AWS Glue Data Catalog integration
- Athena-based serverless SQL analytics
- Data partitioning and organization strategies
- Separation of raw, processed, and business-ready datasets

### 🤖 Generative AI & RAG

- Amazon Bedrock integration patterns for Generative AI
- Retrieval-Augmented Generation (RAG)
- OpenSearch-based semantic retrieval
- Embedding-based knowledge retrieval
- Claims and policy context construction
- Grounded AI responses with validation and business filtering
- Controlled handling of AI and retrieval failures

### 🧠 Agentic Decisioning

- Intelligent claims triage
- Risk and priority evaluation
- Deterministic decision engine
- Escalation and manual-review workflows
- AI-assisted claims analysis
- Decision reasoning and audit traceability
- Workflow orchestration patterns for agentic processing

### 🚀 Application & Engineering

- FastAPI-based application API
- Streamlit user interface
- Dockerized API and UI services
- Pinned application dependencies for reproducibility
- Automated Python application testing
- GitHub Actions CI/CD
- Terraform formatting and validation in CI
- Production-oriented logging, observability, and error handling

## Architecture

ClaimsIQ follows a layered architecture that separates the **AWS infrastructure foundation, data platform, AI intelligence, decisioning, and application layers**.

The design is intended to keep infrastructure concerns separate from business logic while allowing the data and AI layers to work together.

```text
                              CLAIMSIQ PLATFORM
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
                 ▼                                         ▼
        Application Layer                          Intelligence Layer
                 │                                         │
        ┌────────┴────────┐                    ┌───────────┴───────────┐
        │                 │                    │                       │
     FastAPI          Streamlit             RAG                    Agentic
        │                 │                    │                    Decisioning
        └────────┬────────┘                    │                       │
                 │                             │                       │
                 └──────────────┬──────────────┴───────────────────────┘
                                │
                                ▼
                       AI / Retrieval Layer
                                │
                    ┌───────────┴───────────┐
                    │                       │
              Amazon Bedrock           OpenSearch
                    │                       │
                    │                Vector Retrieval
                    │                       │
                    └───────────┬───────────┘
                                │
                                ▼
                       Context & Knowledge
                                │
                                ▼
                    Claims Decisioning Layer
                                │
                  ┌─────────────┼─────────────┐
                  │             │             │
                  ▼             ▼             ▼
                Risk         Priority      Escalation
              Evaluation    Evaluation    / Manual Review
                  │             │             │
                  └─────────────┼─────────────┘
                                ▼
                         Audit / Traceability


                         DATA PLATFORM
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
           Batch            Streaming          Documents
             │                  │                  │
             ▼                  ▼                  ▼
            S3               Kinesis              S3
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼
                           Bronze Layer
                                │
                                ▼
                           Silver Layer
                                │
                                ▼
                            Gold Layer
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                 Athena              BI / Analytics


                      AWS PLATFORM FOUNDATION
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
        ▼                       ▼                        ▼
       VPC                   Compute                 Storage
        │                       │                        │
 Public / Private          EC2 + ASG                  S3
   Subnets                    ALB                     RDS
        │                       │
 Route Tables / NAT       Target Groups
        │
        ▼
 Security Groups / IAM

                                │
                                ▼
                         CloudWatch
                    Monitoring & Observability


                       DELIVERY & IaC
                                │
                     ┌──────────┴──────────┐
                     ▼                     ▼
                  GitHub              Terraform
                     │                     │
                     ▼                     ▼
              GitHub Actions       AWS Infrastructure

Architecture flow

At a high level, the platform works like this:

Claims and related enterprise data enter through batch, streaming, and document ingestion patterns.
Data is organized through the Bronze → Silver → Gold data lake layers.
The AI/RAG layer retrieves relevant claims and policy knowledge using semantic retrieval.
Generative AI uses the retrieved context to assist with analysis and responses.
The decisioning layer evaluates risk, priority, and workflow conditions.
Claims requiring additional attention can be routed toward escalation or manual review.
Decisions and processing information are captured for auditability and traceability.
The application layer exposes these capabilities through FastAPI and Streamlit.
The underlying AWS platform provides the networking, compute, storage, security, and observability foundation.
Terraform and GitHub Actions provide the Infrastructure as Code and CI/CD foundation.
Architectural principle

A key design principle is to keep Generative AI and deterministic business decisioning separate.

Generative AI is used for knowledge retrieval, context understanding, and intelligent assistance, while critical business decisions remain governed by explicit rules and controlled decisioning logic.

This allows ClaimsIQ to combine the flexibility of Generative AI with the predictability and traceability expected from an enterprise claims platform.

## Technology Stack

### ☁️ Cloud & Infrastructure

- Amazon Web Services (AWS)
- Amazon VPC
- Amazon EC2
- EC2 Auto Scaling
- Application Load Balancer
- Amazon S3
- Amazon RDS
- AWS IAM
- Amazon CloudWatch
- Terraform
- Infrastructure as Code (IaC)

### 🗄️ Data Engineering & Analytics

- Amazon S3 Data Lake
- Bronze / Silver / Gold data layers
- Amazon Kinesis Data Streams
- AWS Glue Data Catalog
- AWS Glue ETL architecture
- Amazon Athena
- Redshift Spectrum architecture
- Batch and streaming ingestion patterns

### 🤖 Generative AI & RAG

- Amazon Bedrock
- Generative AI
- Retrieval-Augmented Generation (RAG)
- OpenSearch vector retrieval
- Embeddings
- Semantic search
- Context construction
- Grounded response generation
- AI response validation

### 🧠 Agentic AI & Decisioning

- Agentic workflow patterns
- Claims triage
- Risk evaluation
- Priority evaluation
- Decision engine
- Escalation workflows
- Manual-review routing
- Audit and decision traceability
- Step Functions orchestration architecture

### 🐍 Application Engineering

- Python 3.12
- FastAPI
- Streamlit
- Pydantic
- pytest
- boto3
- OpenSearch Python client

### 🐳 DevOps & Delivery

- Docker
- Docker Compose
- Git
- GitHub
- GitHub Actions
- Terraform validation and formatting
- Reproducible dependency management

## Repository Structure

```text
ClaimsIQ-v2-Enterprise/
│
├── .github/
│   └── workflows/
│       └── terraform.yml
│
├── api/
│   └── FastAPI application
│
├── ui/
│   └── Streamlit application
│
├── src/
│   ├── RAG components
│   ├── decisioning components
│   ├── audit and traceability
│   └── application utilities
│
├── rag/
│   └── Generative AI and retrieval components
│
├── tests/
│   └── application and business-logic tests
│
├── architecture/
│   └── architecture documentation
│
├── docs/
│   └── project and operational documentation
│
├── docker/
│   ├── Dockerfile.api
│   └── Dockerfile.ui
│
├── terraform/
│   ├── envs/
│   │   └── dev/
│   │
│   ├── modules/
│   │   ├── foundation/
│   │   ├── compute/
│   │   ├── storage/
│   │   ├── monitoring/
│   │   └── analytics/
│   │
│   ├── scripts/
│   ├── main.tf
│   ├── providers.tf
│   ├── versions.tf
│   └── outputs.tf
│
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── LICENSE

## Project Highlights

- Designed an end-to-end **AWS cloud architecture** for an intelligent insurance claims platform
- Built modular **Terraform Infrastructure as Code** covering networking, compute, storage, security, and monitoring
- Designed a layered **S3 Data Lake** using Bronze, Silver, and Gold data zones
- Incorporated batch, streaming, and document ingestion patterns for claims-related data
- Implemented application-level **Generative AI and RAG capabilities** for claims and policy knowledge retrieval
- Integrated **OpenSearch-based semantic retrieval** to provide relevant context for AI responses
- Designed **agentic claims decisioning patterns** covering triage, risk evaluation, prioritization, escalation, and manual review
- Kept critical business decisions behind **deterministic decisioning logic** rather than relying entirely on LLM output
- Added **audit and traceability** capabilities for AI-assisted and rule-based decisions
- Built a **FastAPI backend and Streamlit UI** for interacting with the platform
- Containerized application services using **Docker and Docker Compose**
- Added **GitHub Actions CI/CD** for Terraform and application validation
- Applied production-oriented practices around **security, observability, error handling, configuration, and dependency reproducibility**

## Current Status

ClaimsIQ has evolved into an end-to-end intelligent claims platform combining **AWS cloud architecture, data engineering, Generative AI, RAG, agentic decisioning, application services, and CI/CD**.

The platform currently covers:

### AWS & Infrastructure

- Modular Terraform Infrastructure as Code
- VPC and public/private subnet architecture
- Route tables and network connectivity
- Security Groups and IAM
- EC2 and Auto Scaling architecture
- Application Load Balancer and Target Groups
- Amazon S3 data lake architecture
- Amazon RDS integration
- CloudWatch monitoring and observability

### Data Platform

- Bronze, Silver, and Gold data lake layers
- Batch and streaming ingestion patterns
- AWS Glue Data Catalog
- AWS Glue ETL architecture
- Amazon Athena analytics
- Enterprise claims and policy data organization

### Generative AI & RAG

- Amazon Bedrock integration
- Embedding-based retrieval
- OpenSearch vector search
- Claims and policy knowledge retrieval
- RAG context construction
- Grounded response generation
- Response validation and business filtering
- Controlled error handling

### Agentic Decisioning

- Intelligent claims triage
- Risk evaluation
- Priority evaluation
- Deterministic decision engine
- Escalation workflows
- Manual-review routing
- AI-assisted claims analysis
- Audit and decision traceability
- Workflow orchestration patterns

### Application & Delivery

- FastAPI application layer
- Streamlit user interface
- Dockerized services
- Automated Python testing
- GitHub Actions CI/CD
- Terraform formatting and validation
- Dependency reproducibility
- Production-oriented observability and error handling

The project is designed as a **production-oriented reference implementation** demonstrating how AWS infrastructure, enterprise data, Generative AI, RAG, and agentic decisioning can be brought together into a single claims-processing platform.

## License

This project is licensed under the MIT License.