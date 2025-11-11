<!--
═══════════════════════════════════════════════════════════════════════════
SYNC IMPACT REPORT
═══════════════════════════════════════════════════════════════════════════
Version Change: 1.0.0 → 1.1.0
Type: MINOR (Added architectural principle: OpenAPI-first API design with FastAPI)

Modified Principles: None

New Principles:
  - NEW: IV. OpenAPI-First API Design

Added Sections:
  - API Specifications (OpenAPI/Swagger requirements)
  - Framework Standards (FastAPI as primary framework)

Updated Sections:
  - Development Constraints (added FastAPI stack requirement)
  - Quality Standards (added OpenAPI documentation requirements)

Templates Requiring Updates:
  ✅ plan-template.md - Added FastAPI framework requirement, OpenAPI checks
  ✅ spec-template.md - Added API contract section, OpenAPI examples field
  ✅ tasks-template.md - Added OpenAPI documentation tasks
  ⚠ speckit.tasks.prompt.md - Review for OpenAPI contract task generation

Follow-up TODOs: None

Rationale:
  - OpenAPI specifications ensure all endpoints are discoverable, well-documented, and
    interoperable with client generators and API exploration tools
  - FastAPI provides automatic OpenAPI schema generation and interactive API docs (Swagger UI)
  - Structured API documentation enables rapid frontend development and API evolution
  - Demo-ready endpoints with live documentation improve audience confidence
═══════════════════════════════════════════════════════════════════════════
-->

# GHW Trivia Constitution

## Core Principles

### I. Code Quality First

**Clean, maintainable code is NON-NEGOTIABLE, even in rapid development:**

- Code MUST be self-documenting with clear variable/function names
- Complex logic MUST include inline comments explaining the "why"
- Magic numbers MUST be replaced with named constants
- Functions MUST do one thing well (single responsibility)
- Code duplication MUST be eliminated through extraction/abstraction
- Error handling MUST be explicit and informative
- No commented-out code in committed files
- Linting and formatting rules MUST pass before commit

**Rationale:** Live demos require code that can be quickly understood, debugged, and
modified on-the-fly. Clean code prevents demo failures and enables rapid iteration.

### II. User Experience Consistency

**Every user interaction MUST follow consistent patterns:**

- Visual design MUST use a consistent color palette, typography, and spacing
- Similar actions MUST behave identically across all screens/components
- User feedback MUST be immediate and clear (loading states, success/error messages)
- Navigation patterns MUST be predictable and intuitive
- Terminology MUST be consistent across UI, labels, and messaging
- Responsive behavior MUST work across target devices/screen sizes
- Accessibility standards MUST be followed (ARIA labels, keyboard navigation, contrast)

**Rationale:** Inconsistent UX confuses demo audiences and undermines credibility.
Consistency enables users to quickly understand and trust the application during
time-constrained demonstrations.

### III. Rapid Development for Live Demos

**Optimize for speed of delivery and demo readiness:**

- Features MUST be independently deployable and demonstrable
- NO formal testing infrastructure required (manual verification acceptable)
- Configuration MUST be environment-based (dev/staging/prod via env vars)
- Mock data MUST be realistic and demo-appropriate
- Demo scenarios MUST be scripted and repeatable
- Rollback MUST be trivial (feature flags, simple reverts)
- Dependencies MUST be minimal and stable
- Setup/deployment MUST be documented in quickstart guides

**Rationale:** Live demos demand working features fast. Formal test suites slow iteration
for short-lived demo projects. Focus energy on visible features, not testing infrastructure.

### IV. OpenAPI-First API Design

**All APIs MUST be fully OpenAPI 3.0+ compatible with comprehensive documentation:**

- Every endpoint MUST have OpenAPI specification (operationId, summary, description)
- Request/response schemas MUST be defined with examples in OpenAPI definitions
- All path parameters, query parameters, and headers MUST be documented with types/constraints
- Error responses MUST include proper HTTP status codes and schemas
- OpenAPI documentation MUST be auto-generated and always in sync with implementation
- API docs MUST be accessible via interactive UI (Swagger/ReDoc) in demo environments
- OpenAPI spec file MUST be committed to repository (openapi.yaml or openapi.json)
- Client libraries MUST be generatable from OpenAPI specification

**Rationale:** OpenAPI specifications make APIs discoverable, self-documenting, and client-
generation ready. Interactive documentation impresses demo audiences and enables rapid
frontend development. Auto-generation ensures documentation never drifts from implementation.

## Development Constraints

**Technology Stack:**

- Backend MUST use FastAPI framework for Python APIs (provides OpenAPI out-of-the-box)
- All APIs MUST be OpenAPI 3.0+ compatible
- Use well-documented, stable frameworks with strong community support
- Prefer batteries-included solutions over custom implementations
- Minimize build complexity (avoid elaborate toolchains when simple ones suffice)

**API Requirements:**

- All endpoints MUST be documented with OpenAPI decorators/annotations
- Pydantic models MUST be used for request/response schemas (automatic JSON Schema conversion)
- API documentation MUST be generated automatically via FastAPI/Swagger
- Endpoint descriptions MUST include usage examples in OpenAPI definitions
- All error codes MUST be documented with proper HTTP status codes

**Performance Targets:**

- Initial page load MUST complete in under 3 seconds on demo network
- User interactions MUST respond in under 200ms
- API endpoints MUST respond in under 500ms (excluding external I/O)
- No memory leaks during extended demo sessions (minimum 30 minutes continuous use)

**Deployment:**

- Deployment MUST be single-command or automated CI/CD
- Environment configuration MUST be externalized (no hardcoded credentials/endpoints)
- Demo data reset MUST be scriptable for quick turnaround between presentations
- OpenAPI spec MUST be accessible at `/openapi.json` endpoint

## Quality Standards

**Code Review Checkpoints:**

- Does this code follow naming conventions and eliminate magic numbers?
- Are error cases handled with clear user feedback?
- Is the UX consistent with existing patterns?
- Can this be demo'd independently?
- Is the quickstart documentation updated?
- (For APIs) Is the OpenAPI specification complete with examples?
- (For APIs) Are all request/response schemas properly documented?
- (For APIs) Can endpoint be tested via interactive API docs?

**API Documentation Requirements:**

- Every endpoint MUST have OpenAPI operationId, summary, and description
- All request schemas MUST include field descriptions and example values
- All response schemas MUST include field descriptions and example values
- Error responses MUST document all possible HTTP status codes (400, 404, 500, etc.)
- Endpoint descriptions SHOULD explain use cases and business logic briefly
- Complex parameters MUST include documentation for constraints (min/max, regex patterns, etc.)

**General Documentation Requirements:**

- Every feature MUST update relevant quickstart guide
- API/component interfaces MUST include usage examples
- Demo scripts MUST be maintained for key user flows
- README MUST reflect current setup/run instructions

**Complexity Justification:**

- Additional frameworks/libraries MUST be justified (why not built-in solution?)
- Architectural patterns MUST solve a demonstrated problem (no speculative engineering)
- External dependencies MUST be stable and necessary

## Governance

**Authority:**

This constitution supersedes all other practices and conventions. When conflict arises
between this document and other guidance, the constitution prevails.

**Amendments:**

- Minor changes (clarifications, examples) increment PATCH version
- New principles or sections increment MINOR version
- Removal or redefinition of principles increments MAJOR version
- All amendments MUST update plan/spec/tasks templates for consistency
- Amendment date updates "Last Amended" field

**Compliance:**

- All pull requests MUST pass code quality linting
- All features MUST include quickstart documentation updates
- Constitution violations MUST be documented in plan.md Complexity Tracking table
- Regular reviews ensure templates align with constitutional principles

**Runtime Guidance:**

For agent-specific development workflows, refer to `.specify/templates/agent-file-template.md`
and command prompt files in `.github/prompts/speckit.*.prompt.md`.

**Version**: 1.0.0 | **Ratified**: 2025-11-11 | **Last Amended**: 2025-11-11
