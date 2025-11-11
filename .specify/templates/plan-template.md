# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: FastAPI (REQUIRED for Python backend), [additional dependencies or N/A]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: N/A (manual verification only - per constitution)  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: Page load <3s, API responses <500ms, interactions <200ms (per constitution)  
**Constraints**: [domain-specific, e.g., demo-ready, mobile-responsive, OpenAPI-compliant or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., demo scenarios, expected user count or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. Code Quality First:**
- [ ] Code uses clear, self-documenting names (no generic vars like `x`, `temp`, `data`)
- [ ] Complex logic has explanatory comments
- [ ] No magic numbers (all constants named)
- [ ] Functions follow single responsibility principle
- [ ] Code duplication eliminated
- [ ] Error handling is explicit with user-friendly messages
- [ ] No commented-out code
- [ ] Linting/formatting rules configured

**II. User Experience Consistency:**
- [ ] Visual design system defined (colors, typography, spacing)
- [ ] Interaction patterns documented and consistent
- [ ] User feedback mechanisms identified (loading, success, errors)
- [ ] Navigation flow is intuitive
- [ ] Terminology is consistent across UI
- [ ] Responsive design strategy defined
- [ ] Accessibility requirements specified (ARIA, keyboard, contrast)

**III. Rapid Development for Live Demos:**
- [ ] Feature can be demo'd independently
- [ ] No formal testing infrastructure required
- [ ] Environment configuration externalized
- [ ] Mock/demo data prepared and realistic
- [ ] Demo scenario scripted
- [ ] Deployment is single-command or automated
- [ ] Dependencies are minimal and stable
- [ ] Quickstart guide will be updated

**IV. OpenAPI-First API Design:**
- [ ] FastAPI framework selected for Python backends
- [ ] All endpoints have OpenAPI operationId, summary, description
- [ ] Request/response schemas defined with Pydantic models
- [ ] Example values included in schema definitions
- [ ] Error responses documented with proper HTTP status codes
- [ ] OpenAPI spec accessible at /openapi.json
- [ ] Interactive API docs (Swagger UI) available
- [ ] Complex parameters documented with constraints

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
