# Grace Alone ABA - End-to-End Test Plan

## Overview

This document defines the comprehensive E2E test plan for the Grace Alone ABA EHR system. Tests are organized by critical path and billing gate enforcement.

---

## TEST ENVIRONMENT SETUP

### Prerequisites
- Test database with seeded data
- Test user accounts for each role
- Test client with active authorization
- Mock clearinghouse for EDI testing

### Test Users
| Email | Password | Role |
|-------|----------|------|
| admin@test.com | TestPass123! | Admin |
| bcba@test.com | TestPass123! | BCBA |
| rbt@test.com | TestPass123! | RBT |
| billing@test.com | TestPass123! | Billing |
| parent@test.com | TestPass123! | Parent |

### Test Data
- Client: "Test Client" (DOB: 2015-01-15)
- Authorization: 100 units of 97153, active
- Payer: "Test Insurance Co"

---

## CRITICAL PATH TESTS

### CP-001: Complete Session-to-Claim Workflow

**Objective:** Verify the complete happy path from session creation to claim submission.

**Preconditions:**
- BCBA user logged in
- Client has active authorization with available units
- Client has active insurance coverage

**Steps:**

1. **Schedule Session**
   - Navigate to Schedule → New Session
   - Select client: "Test Client"
   - Select service code: 97153
   - Set date: Today
   - Set time: 9:00 AM - 11:00 AM
   - Link authorization
   - Save session

   **Expected:** Session created with status "scheduled"

2. **Clock In (RBT)**
   - Login as RBT
   - Navigate to Today's Sessions
   - Click "Clock In" on the session
   - Allow geolocation capture

   **Expected:** Session status changes to "in_progress", clock-in time and location recorded

3. **Clock Out (RBT)**
   - After service, click "Clock Out"
   - Allow geolocation capture

   **Expected:** Session status changes to "completed", duration calculated

4. **Complete Clinical Note (RBT)**
   - Navigate to session → Create Note
   - Enter SOAP note content:
     - Subjective: Parent reports...
     - Objective: Data collected...
     - Assessment: Progress toward goals...
     - Plan: Continue intervention...
   - Save as draft

   **Expected:** Note created with status "draft"

5. **Submit Note for Signature**
   - Click "Submit for Signature"

   **Expected:** Note status changes to "pending_signature"

6. **Sign and Lock Note (BCBA)**
   - Login as BCBA (supervising)
   - Navigate to Notes → Pending Signature
   - Review note content
   - Click "Sign and Lock"
   - Enter attestation: "I attest that this note accurately reflects..."

   **Expected:**
   - Note status changes to "locked"
   - Content hash generated
   - locked_at timestamp set
   - Note becomes immutable

7. **Generate Claim (Billing)**
   - Login as Billing user
   - Navigate to Billing → Generate Claims
   - Select the completed session
   - Click "Generate Claim"

   **Expected:**
   - All billing gates pass
   - Claim created with status "draft"
   - Authorization units consumed
   - Ledger entry created

8. **Scrub Claim**
   - Click "Scrub" on the claim

   **Expected:** Scrubber returns passed with 0 errors

9. **Submit Claim**
   - Click "Submit for Processing"

   **Expected:** Claim status changes to "ready_to_submit"

**Postconditions:**
- Authorization units decreased
- Claim in submission queue
- Full audit trail exists

---

## BILLING GATE TESTS

### BG-001: Block Claim - Session Not Completed

**Objective:** Verify claims cannot be generated from incomplete sessions.

**Steps:**
1. Create a session with status "scheduled"
2. Attempt to generate claim via API:
   ```
   POST /api/v1/claims/generate_from_session/
   {"session_id": "<scheduled_session_id>"}
   ```

**Expected Response:**
```json
{
  "error": "BILLING GATE FAILED: Session not completed",
  "gate": "session_completed",
  "current_status": "scheduled",
  "required_status": "completed"
}
```
**Status Code:** 400

---

### BG-002: Block Claim - Note Not Locked

**Objective:** Verify claims cannot be generated when note is not locked.

**Steps:**
1. Create completed session with draft note
2. Attempt to generate claim

**Expected Response:**
```json
{
  "error": "BILLING GATE FAILED: Clinical note not locked",
  "gate": "note_locked",
  "current_status": "draft",
  "required_status": "locked"
}
```
**Status Code:** 400

---

### BG-003: Block Claim - No Clinical Note

**Objective:** Verify claims cannot be generated without a clinical note.

**Steps:**
1. Create completed session with no note
2. Attempt to generate claim

**Expected Response:**
```json
{
  "error": "BILLING GATE FAILED: No clinical note found",
  "gate": "note_exists"
}
```
**Status Code:** 400

---

### BG-004: Block Claim - Authorization Not Active

**Objective:** Verify claims cannot be generated with inactive authorization.

**Steps:**
1. Create completed session with locked note
2. Set authorization status to "expired"
3. Attempt to generate claim

**Expected Response:**
```json
{
  "error": "BILLING GATE FAILED: Authorization not active",
  "gate": "authorization_active"
}
```
**Status Code:** 400

---

### BG-005: Block Claim - Insufficient Units

**Objective:** Verify claims cannot be generated when authorization has insufficient units.

**Steps:**
1. Create completed session with locked note
2. Set authorization available_units to 0
3. Attempt to generate claim

**Expected Response:**
```json
{
  "error": "BILLING GATE FAILED: Insufficient authorization units",
  "gate": "authorization_units",
  "units_requested": 8.0,
  "units_available": 0.0
}
```
**Status Code:** 400

---

### BG-006: Block Claim - Service Code Mismatch

**Objective:** Verify claims cannot be generated when service codes don't match.

**Steps:**
1. Create session with service code 97153
2. Link authorization for service code 97155
3. Attempt to generate claim

**Expected Response:**
```json
{
  "error": "BILLING GATE FAILED: Service code mismatch",
  "gate": "service_code_match",
  "session_code": "97153",
  "authorization_code": "97155"
}
```
**Status Code:** 400

---

## NOTE IMMUTABILITY TESTS

### NI-001: Block Edit on Locked Note

**Objective:** Verify locked notes cannot be modified via API.

**Steps:**
1. Create and lock a clinical note
2. Attempt to update note:
   ```
   PATCH /api/v1/notes/<note_id>/
   {"objective": "Modified content"}
   ```

**Expected Response:**
```json
{
  "error": "FORBIDDEN: Locked notes cannot be modified.",
  "message": "Use the add_addendum endpoint to add corrections or additional information."
}
```
**Status Code:** 403

---

### NI-002: Block Delete on Locked Note

**Objective:** Verify locked notes cannot be deleted.

**Steps:**
1. Create and lock a clinical note
2. Attempt to delete:
   ```
   DELETE /api/v1/notes/<note_id>/
   ```

**Expected Response:**
```json
{
  "error": "Locked notes cannot be deleted"
}
```
**Status Code:** 403

---

### NI-003: Addendum Creation

**Objective:** Verify addendums can be added to locked notes.

**Steps:**
1. Create and lock a clinical note
2. Add addendum:
   ```
   POST /api/v1/notes/<note_id>/add_addendum/
   {
     "reason": "correction",
     "content": "Correction: Client's name was misspelled."
   }
   ```

**Expected:**
- Addendum created with timestamp
- Original note content unchanged
- Addendum linked to note

---

### NI-004: Content Hash Verification

**Objective:** Verify content hash detects tampering.

**Steps:**
1. Create and lock a clinical note
2. Verify integrity:
   ```
   GET /api/v1/notes/<note_id>/verify_integrity/
   ```

**Expected Response:**
```json
{
  "is_valid": true,
  "stored_hash": "abc123...",
  "current_hash": "abc123...",
  "message": "Content integrity verified"
}
```

---

## SESSION OVERLAP TESTS

### SO-001: Block Overlapping Client Sessions

**Objective:** Verify same client cannot have overlapping sessions.

**Steps:**
1. Create session for Client A: 9:00-10:00
2. Attempt to create second session for Client A: 9:30-10:30

**Expected Response:**
```json
{
  "error": "Client already has a session scheduled during this time."
}
```
**Status Code:** 400

---

### SO-002: Block Overlapping Provider Sessions

**Objective:** Verify same provider cannot have overlapping sessions.

**Steps:**
1. Create session with Provider A, Client A: 9:00-10:00
2. Attempt to create session with Provider A, Client B: 9:30-10:30

**Expected Response:**
```json
{
  "error": "Provider already has a session scheduled during this time."
}
```
**Status Code:** 400

---

## ROLE-BASED ACCESS TESTS

### RBA-001: RBT Cannot Access Unassigned Clients

**Objective:** Verify RBTs can only see assigned clients.

**Steps:**
1. Login as RBT
2. Attempt to access unassigned client:
   ```
   GET /api/v1/clients/<unassigned_client_id>/
   ```

**Expected:** 403 Forbidden or 404 Not Found

---

### RBA-002: Parent Can Only See Own Child

**Objective:** Verify parents can only access their own child's data.

**Steps:**
1. Login as Parent
2. Attempt to access different client:
   ```
   GET /api/v1/clients/<other_client_id>/
   ```

**Expected:** 403 Forbidden or 404 Not Found

---

### RBA-003: Billing Cannot See Note Content

**Objective:** Verify billing role sees limited note fields.

**Steps:**
1. Login as Billing user
2. Request clinical note:
   ```
   GET /api/v1/notes/<note_id>/
   ```

**Expected:** Response excludes clinical content fields (subjective, objective, assessment, plan)

---

### RBA-004: RBT Cannot Sign BCBA Notes

**Objective:** Verify RBTs cannot sign notes they didn't author.

**Steps:**
1. Login as RBT
2. Attempt to sign note authored by BCBA:
   ```
   POST /api/v1/notes/<bcba_note_id>/sign_and_lock/
   ```

**Expected:** 403 Forbidden

---

## AUTHORIZATION LEDGER TESTS

### AL-001: Unit Consumption Creates Ledger Entry

**Objective:** Verify unit consumption is recorded immutably.

**Steps:**
1. Check authorization available_units: 100
2. Generate claim for 8 units
3. Query ledger:
   ```
   GET /api/v1/authorizations/<auth_id>/ledger/
   ```

**Expected:**
- Ledger entry with transaction_type: "consume"
- units: 8
- balance_after: 92

---

### AL-002: Unit Reversal on Claim Void

**Objective:** Verify voiding claim reverses units.

**Steps:**
1. Generate claim consuming 8 units
2. Void the claim
3. Check authorization available_units

**Expected:**
- Units restored to original
- Ledger entry with transaction_type: "reverse"
- Reason includes void explanation

---

## AI GOVERNANCE TESTS

### AI-001: Permitted Action - Summarize

**Objective:** Verify AI can summarize existing content.

**Steps:**
1. Submit AI request:
   ```
   POST /api/v1/ai/assist/
   {
     "action": "summarize_session_note",
     "input": "<existing note content>"
   }
   ```

**Expected:**
- Request succeeds
- AI audit log entry created
- Response requires human attestation

---

### AI-002: Block Forbidden Action - Generate Clinical

**Objective:** Verify AI cannot generate clinical content from scratch.

**Steps:**
1. Submit AI request:
   ```
   POST /api/v1/ai/assist/
   {
     "action": "generate_clinical_content",
     "input": "Write a session note for today"
   }
   ```

**Expected Response:**
```json
{
  "error": "FORBIDDEN: This action is not permitted",
  "action": "generate_clinical_content",
  "message": "AI cannot generate clinical observations or data"
}
```
**Status Code:** 403

---

### AI-003: AI Audit Trail Completeness

**Objective:** Verify AI audit logs capture all required fields.

**Steps:**
1. Perform permitted AI action
2. Query AI audit log

**Expected fields:**
- user_id
- timestamp
- model_version
- prompt_input
- ai_output
- user_decision (accept/reject)
- human_attested
- unique_content_percentage

---

## PUBLIC WEBSITE TESTS

### PW-001: Contact Form Submission

**Objective:** Verify contact form submits successfully.

**Steps:**
1. Navigate to /contact
2. Fill form with valid data
3. Submit

**Expected:**
- Success message displayed
- Lead record created in database

---

### PW-002: PHI Detection Block

**Objective:** Verify PHI is blocked in contact form.

**Steps:**
1. Navigate to /contact
2. Enter text containing SSN pattern in notes field
3. Submit

**Expected:**
- Submission blocked
- Error message about PHI

---

## SECURITY TESTS

### SEC-001: Account Lockout After Failed Attempts

**Objective:** Verify account locks after 5 failed login attempts.

**Steps:**
1. Attempt login with wrong password 5 times
2. Attempt login with correct password

**Expected:**
- After 5th failure: account locked message
- Correct password still fails with locked message

---

### SEC-002: Session Timeout

**Objective:** Verify sessions expire after inactivity.

**Steps:**
1. Login and get access token
2. Wait 61 minutes (or mock time)
3. Attempt authenticated request

**Expected:** 401 Unauthorized - token expired

---

### SEC-003: CSRF Protection

**Objective:** Verify CSRF tokens are required for mutations.

**Steps:**
1. Attempt POST without CSRF token (if using session auth)

**Expected:** 403 Forbidden - CSRF token missing

---

## AUDIT LOG TESTS

### AUD-001: Login Attempts Logged

**Objective:** Verify all login attempts are logged.

**Steps:**
1. Attempt successful login
2. Attempt failed login
3. Query audit logs

**Expected:**
- Both attempts logged
- IP address captured
- User agent captured
- Timestamp accurate

---

### AUD-002: PHI Access Logged

**Objective:** Verify all PHI access is logged.

**Steps:**
1. Access client record
2. Query PHI access log

**Expected:**
- Access logged with user, resource, action
- Fields accessed recorded
- Timestamp accurate

---

### AUD-003: Audit Logs Immutable

**Objective:** Verify audit logs cannot be modified or deleted.

**Steps:**
1. Attempt to modify audit log via admin
2. Attempt to delete audit log via admin

**Expected:**
- Modifications blocked
- Deletions blocked
- Error message indicates immutability

---

## PERFORMANCE TESTS

### PERF-001: Dashboard Load Time

**Objective:** Dashboard loads within acceptable time.

**Criteria:** < 2 seconds for initial load

---

### PERF-002: Session List Performance

**Objective:** Session list handles large datasets.

**Steps:**
1. Seed 10,000 sessions
2. Load session list with pagination

**Criteria:** < 500ms response time

---

### PERF-003: Claim Generation Performance

**Objective:** Claim generation completes quickly.

**Criteria:** < 1 second per claim

---

## TEST EXECUTION MATRIX

| Test ID | Priority | Automation | Environment |
|---------|----------|------------|-------------|
| CP-001 | Critical | Cypress | Staging |
| BG-001 - BG-006 | Critical | Pytest | All |
| NI-001 - NI-004 | Critical | Pytest | All |
| SO-001 - SO-002 | High | Pytest | All |
| RBA-001 - RBA-004 | Critical | Pytest | All |
| AL-001 - AL-002 | High | Pytest | All |
| AI-001 - AI-003 | High | Pytest | Staging |
| PW-001 - PW-002 | Medium | Cypress | All |
| SEC-001 - SEC-003 | Critical | Pytest | All |
| AUD-001 - AUD-003 | Critical | Pytest | All |
| PERF-001 - PERF-003 | Medium | k6 | Staging |

---

## REGRESSION TEST SCHEDULE

| Frequency | Tests |
|-----------|-------|
| Every PR | BG-*, NI-*, SO-*, RBA-* |
| Daily | CP-001, SEC-*, AUD-* |
| Weekly | All tests |
| Pre-release | All tests + PERF-* |

---

## SIGN-OFF REQUIREMENTS

Before production deployment:
- [ ] All Critical tests passing
- [ ] All High priority tests passing
- [ ] No Critical or High bugs open
- [ ] Performance benchmarks met
- [ ] Security scan passed
- [ ] HIPAA compliance verified
