---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Per GHW Trivia constitution, this project uses MANUAL VERIFICATION ONLY. No automated test tasks will be included.

**Code Quality**: All tasks must adhere to constitutional principles (clean code, UX consistency, demo-readiness).

**Organization**: Tasks are grouped by user story to enable independent implementation and manual verification of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Manually verified independently
  - Delivered as an MVP increment
  
  NO AUTOMATED TEST TASKS: Per constitution, this project uses manual verification.
  Focus on code quality gates (linting, formatting, code review) instead.
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize FastAPI project with dependencies (fastapi, pydantic, uvicorn)
- [ ] T003 [P] Configure linting and formatting tools (constitution requirement)
- [ ] T004 [P] Setup code quality pre-commit hooks
- [ ] T005 [P] Configure OpenAPI/Swagger documentation generation
- [ ] T006 Create base FastAPI app with OpenAPI info (title, description, version)
- [ ] T007 Setup OpenAPI response models and error schemas

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T008 Setup database schema and migrations framework
- [ ] T009 [P] Implement authentication/authorization framework
- [ ] T010 [P] Setup API routing and middleware structure (FastAPI routers)
- [ ] T011 Create base models/entities that all stories depend on
- [ ] T012 Configure error handling and logging infrastructure
- [ ] T013 Setup environment configuration management
- [ ] T014 [P] Define UX design system (colors, typography, spacing - per constitution)
- [ ] T015 [P] Create reusable UI components for consistent UX
- [ ] T016 Prepare realistic demo/mock data
- [ ] T017 [P] Define common Pydantic schemas for request/response (OpenAPI)
- [ ] T018 Create error response schemas (400, 404, 500, etc. with OpenAPI docs)

**Code Quality Gate**: Run linting/formatting checks before proceeding

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Manual Verification Plan**: [How to manually verify this story works - specific steps]

### Implementation for User Story 1

- [ ] T019 [P] [US1] Create [Entity1] model in src/models/[entity1].py
- [ ] T020 [P] [US1] Create [Entity2] model in src/models/[entity2].py
- [ ] T021 [US1] Implement [Service] in src/services/[service].py (depends on T019, T020)
- [ ] T022 [US1] Implement [endpoint] in src/api/endpoints/[endpoint].py with OpenAPI decorators
- [ ] T023 [P] [US1] Define Pydantic request/response models in src/schemas/[entity].py
- [ ] T024 [US1] Add OpenAPI operationId, summary, description for all endpoints
- [ ] T025 [US1] Add example values and constraints to Pydantic models
- [ ] T026 [US1] Document error responses (400, 404, 500) with OpenAPI status codes
- [ ] T027 [US1] Add validation and user-friendly error handling
- [ ] T028 [US1] Add logging for user story 1 operations
- [ ] T029 [P] [US1] Implement UI components with consistent design system
- [ ] T030 [US1] Add loading states and user feedback mechanisms
- [ ] T031 [US1] Implement accessibility features (ARIA, keyboard nav)
- [ ] T032 [US1] Verify OpenAPI docs auto-generated at /docs endpoint
- [ ] T033 [US1] Update quickstart.md with API usage examples and demo instructions

**Code Quality Gate**: 
- [ ] Run linting/formatting checks
- [ ] Code review for naming conventions, no magic numbers
- [ ] Verify UX consistency with design system
- [ ] Verify OpenAPI documentation is complete and accurate

**Manual Verification Checkpoint**: 
- [ ] Demo User Story 1 following verification plan
- [ ] Test all endpoints via Swagger UI at /docs
- [ ] Verify user feedback is clear and immediate
- [ ] Check accessibility (keyboard, screen reader)
- [ ] Test responsive design on target devices
- [ ] Verify OpenAPI spec can be consumed by client generators

**Checkpoint**: At this point, User Story 1 should be fully functional and demo-ready

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Manual Verification Plan**: [How to manually verify this story works]

### Implementation for User Story 2

- [ ] T034 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T035 [US2] Implement [Service] in src/services/[service].py
- [ ] T036 [US2] Implement [endpoint] in src/api/endpoints/[endpoint].py with OpenAPI decorators
- [ ] T037 [P] [US2] Define Pydantic request/response models in src/schemas/[entity].py
- [ ] T038 [US2] Add OpenAPI operationId, summary, description, and examples
- [ ] T039 [US2] Document error responses with proper HTTP status codes
- [ ] T040 [US2] Integrate with User Story 1 components (if needed)
- [ ] T041 [P] [US2] Implement UI with consistent patterns from US1
- [ ] T042 [US2] Add error handling with clear user messaging
- [ ] T043 [US2] Update quickstart.md with new demo scenarios and API examples

**Code Quality Gate**: 
- [ ] Run linting/formatting checks
- [ ] Code review for code quality principles
- [ ] Verify UX consistency across US1 and US2
- [ ] Verify OpenAPI documentation is complete

**Manual Verification Checkpoint**:
- [ ] Demo User Story 2 independently
- [ ] Test all endpoints via Swagger UI at /docs
- [ ] Demo combined US1 + US2 flow
- [ ] Verify consistent UX patterns

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Manual Verification Plan**: [How to manually verify this story works]

### Implementation for User Story 3

- [ ] T044 [P] [US3] Create [Entity] model in src/models/[entity].py
- [ ] T045 [US3] Implement [Service] in src/services/[service].py
- [ ] T046 [US3] Implement [endpoint] in src/api/endpoints/[endpoint].py with OpenAPI decorators
- [ ] T047 [P] [US3] Define Pydantic request/response models in src/schemas/[entity].py
- [ ] T048 [US3] Add complete OpenAPI documentation and examples
- [ ] T049 [P] [US3] Implement UI maintaining design consistency
- [ ] T050 [US3] Update quickstart.md with complete demo flow

**Code Quality Gate**: 
- [ ] Run linting/formatting checks
- [ ] Final code review for all quality principles
- [ ] Verify complete UX consistency
- [ ] Verify complete OpenAPI documentation

**Manual Verification Checkpoint**:
- [ ] Demo User Story 3 independently
- [ ] Test all endpoints via Swagger UI
- [ ] Demo complete application flow (all stories)
- [ ] Verify all user feedback mechanisms work

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Final documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring (remove duplication, improve naming)
- [ ] TXXX Performance optimization across all stories (verify <3s load, <500ms API, <200ms interactions)
- [ ] TXXX Security hardening
- [ ] TXXX Final accessibility audit across all features
- [ ] TXXX Generate and review complete OpenAPI spec (openapi.json or openapi.yaml)
- [ ] TXXX Verify ReDoc documentation (alternative to Swagger UI)
- [ ] TXXX Run complete quickstart.md validation
- [ ] TXXX Prepare demo script for live presentation
- [ ] TXXX Test demo scenario end-to-end with realistic data

**Final Code Quality Gate**:
- [ ] All linting/formatting rules pass
- [ ] No commented-out code
- [ ] All magic numbers replaced with constants
- [ ] All error messages are user-friendly
- [ ] Code review complete
- [ ] All endpoints have complete OpenAPI documentation

**Final Manual Verification**:
- [ ] Complete demo run-through (time it)
- [ ] Verify all user flows work smoothly
- [ ] Check all error states show clear messages
- [ ] Confirm consistent UX across entire app
- [ ] Test deployment from scratch
- [ ] Verify OpenAPI spec is accurate and complete
- [ ] Test client generation from OpenAPI spec (if applicable)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- UI components with design system consistency
- Code quality gates before moving to verification
- Manual verification before story completion
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- UI components within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"

# Launch all UI components for User Story 1 together:
Task: "Implement UI components with consistent design system"
Task: "Add loading states and user feedback mechanisms"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Manually verify User Story 1 following demo plan
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Manually verify independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Manually verify independently → Deploy/Demo
4. Add User Story 3 → Manually verify independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and manually verifiable
- Code quality gates (linting/formatting) at each checkpoint
- Manual verification required before story completion
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently via demo
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
