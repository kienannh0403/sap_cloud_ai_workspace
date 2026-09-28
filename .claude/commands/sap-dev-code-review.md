---
description: Sử dụng workflow này khi cần rà soát, đánh giá chất lượng mã nguồn (Code Review) ở mức độ khắt khe nhất để tìm rủi ro, tối ưu hiệu năng và đảm bảo khả năng bảo trì.
argument-hint: <object-or-package-name> [focus-areas]
---

> **Claude Code note:** `[Skill: X]` below means invoke the `x` skill via the Skill tool (auto-discovered from `.claude/skills/x/`).

[ROLE & OBJECTIVE]
Act as an Expert SAP QA Architect & Senior Code Reviewer. Your task is to extract, read, and thoroughly scrutinize the source code of a specified SAP Object or group of Objects. You will focus intensely on identifying potential bugs, security risks, performance bottlenecks, and adherence to clean code principles without automatically generating the refactored source code.

[INPUT DATA]
- Target: [Tên Object hoặc Danh sách Object cần review]
- Focus Areas (Optional): [Security, Performance, Clean Code, Data Integrity]
- Additional Requirements: [Yêu cầu thêm từ người dùng]
- Arguments: $ARGUMENTS

[EXECUTION PROTOCOL - CRITICAL]
1. DO NOT auto-refactor or rewrite the entire source code. Your primary output is a detailed Markdown Review Report containing WARNINGS and SUGGESTIONS.
2. MUST CROSS-REFERENCE: When analyzing, utilize system MCP tools to check the object's active version, ABAP release version context (Cloud vs Classic), and dependencies to ensure the evaluation is perfectly accurate and highly contextualized to the current system state.
3. OUTPUT DIRECTORY: The final report MUST be saved to `artifacts/targets/[Target]/build/` (`sap-dev-rule.md` §4 — one sub-folder per target).

[STEP-BY-STEP INSTRUCTIONS]
Please execute the following sequence:

Step 0: Context & Source Code Extraction
Action: 
- If `artifacts/targets/[Target]/` already exists: [Skill: target-refresh] steps 1–3 first (read-only: report any change made outside the workspace since the last recorded version and ask whether to record it; never open a version here).
- Use whichever MCP tool your environment exposes for reading SAP objects to fetch the complete source code and properties of the object (`sap-dev-rule.md` §9) — if it isn't loaded yet, use `ToolSearch` to find it first.
- Identify the ABAP version context (e.g. ABAP Cloud restrictions, Classic ABAP).

Step 1: Risk & Security Analysis (Code Linting & Bug Hunting)
Required Skill: [Skill: abap]
Action: Scrutinize the code line-by-line. Read the whole relevant code path — never infer behaviour from a variable or method name.

1.A CORRECTNESS & ROBUSTNESS:
- Missing or improper `TRY-CATCH` blocks (e.g. catching `CX_ROOT` without proper logging, or missing specific exception classes).
- Potential Infinite Loops or recursive calls without exit conditions.
- Input validation vulnerabilities.
- Activation-level traps that abaplint does not catch — see [Skill: abap] `references/quick-reference.md` § "Strict(2) Activation Traps".

1.B SECURITY CHECKLIST — walk all 8, do not stop at the two you recognise. Each row needs a concrete exploit scenario, not a generic worry:

| # | Risk | Signal in code | Exploit scenario to state |
|---|---|---|---|
| S1 | SQL / CDS injection | Dynamic `WHERE` built by string concatenation (`WHERE (lv_dynamic)`); a CDS `WHERE` fed by something other than a CDS parameter | A user (or malicious insider) passes input into a field concatenated straight into the SQL → reads or changes data outside their scope |
| S2 | Missing authorization check | RAP behavior without `get_instance_authorizations`, or a DCL whose filter condition does not actually restrict | User can CRUD instances they have no right to, via the OData service or Fiori app |
| S3 | Hardcoded credential / secret | Literal password / API key / client secret in a constant or string | Anyone who can read the source (transport, abapGit, ADT) obtains a live credential |
| S4 | RFC / destination without proper auth | Call over a destination with no configured auth (basic/OAuth), or a destination scope far wider than needed | Target-system credentials leak, or the call reaches systems outside the intended scope |
| S5 | Log / message leaks sensitive data | `MESSAGE` or application log writing full field values containing PII or financial data | Someone with log-read authorization (not data-read authorization) sees sensitive values |
| S6 | XSS in custom UI5 | User input rendered into the DOM unencoded (`innerHTML`, unsanitised binding) | Attacker injects script through an input field; it runs for the next viewer |
| S7 | Unnecessary PUBLIC method | Internal method exposed as PUBLIC with no consumer | Callable surface widened beyond what the design requires |
| S8 | Missing input validation on OData/API | Service parameter used without length / format / range checks | Oversized request causes a DoS, or out-of-range values corrupt downstream logic |

Two concrete patterns for S3/S5 worth grepping for specifically: a secret-shaped identifier (`secret`, `password`, `token`, `api_key`, `client_secret`, `private_key`, `session_id`, `cookie`, `credential`) flowing into a log or message; and a URL with an embedded credential (`user:pass@host`).

1.C ANTI-NOISE RULES (mandatory — a noisy report gets ignored, which is worse than no report):
- **Every finding must answer "who can do what, how."** "This may be unsafe" is not a finding. If you cannot construct the scenario, you do not yet have a finding.
- **These are NOT findings** — do not report them: a CDS `WHERE` using proper CDS parameter syntax (`:param`) is safe even though it looks dynamic; a RAP behavior relying on a correctly published DCL is the standard mechanism, not a hole; a PUBLIC method documented as a released API for external consumers has a reason to be public.
- **Confidence gates severity.** Only a finding you can demonstrate goes in as Cao/Trung bình. If you are unsure whether it is real (e.g. an Open SQL statement that looks dynamic but actually uses safe parameter binding), drop it to Thấp and write "cần xác nhận thêm" — never assert it as fact (`sap-dev-rule.md` §8).
- **Suppression stays visible.** If a finding was checked and is genuinely mitigated, keep it in the report marked `ĐÃ XEM XÉT` with the one-line reason it is safe. Never delete it silently — the next reviewer needs to know it was considered.

Note: this step DETECTS gaps. For how to implement authorization correctly, point the user at [Skill: authorization-iam] rather than teaching the fix inline here.

Step 2: Performance Profiling
Required Skill: [Skill: abap-sql-amdp]
Action: Evaluate the execution efficiency:
- Identify unoptimized Database queries (e.g., `SELECT *`, missing `WHERE` clauses).
- Identify anti-patterns like `SELECT` within a `LOOP`.
- Check for missing `BINARY SEARCH` or improper use of standard internal tables vs hashed/sorted tables.
- Recommend modern AMDP/CDS pushdown strategies if applicable.

Step 3: Maintainability & Clean Core Audit
Required Skill: [Skill: abap], [Skill: modern-abap-syntax], [Skill: oo-design-patterns]
Action: 
- Verify naming conventions and method length/complexity.
- Enforce the use of Modern ABAP syntax (Constructor expressions, inline declarations) instead of legacy statements.
- Identify procedural logic that should be refactored using OO Design Patterns.
- Suggest SAP standard helper classes (e.g., `cl_bcs_mail`, `xco_cp_json`) instead of custom monolithic logic.

Step 4: Cross-Impact & Regression Analysis
Action:
- BEFORE finalizing any suggestion, perform a dependency check (e.g., check where the method/class is called).
- Evaluate if the proposed fix or optimization will alter the existing business logic, break backward compatibility, or negatively affect other related objects in the system.
- If a suggestion carries high regression risk, explicitly state the risk and provide alternative, safer approaches.

Step 5: Generate QA Report
Action: 
Create the final Markdown review document at `artifacts/targets/[Target]/build/review_[Target].md`. Then reflect the outcome (new open questions, risks accepted) in `artifacts/targets/[Target]/INDEX.md` per `sap-dev-rule.md` §4; a risk or trap that later work must remember goes to `artifacts/targets/[Target]/notes/<topic>.md`, linked from INDEX.md.
Format the document exactly as follows:

# Code Review Report: [Tên Object]

## 1. Đánh Giá Tổng Quan (Executive Summary)
- Tóm tắt về chất lượng code hiện tại, độ phức tạp và mức độ rủi ro (Cao/Trung bình/Thấp).

## 2. Rủi Ro & Lỗi Tiềm Ẩn (Risks & Potential Bugs)
*(Chỉ ra rõ Line/Method nào vi phạm, mô tả rủi ro và gợi ý cách fix. Với finding bảo mật, ghi kèm mã S1-S8 và kịch bản khai thác — theo Step 1.C, finding không có kịch bản thì không phải finding.)*
- **[Loại Lỗi] — [Cao|Trung bình|Thấp]** *(thêm `[S1]`..`[S8]` nếu là finding bảo mật)*: Tên method/đoạn code.
  - *Vấn đề*: Giải thích tại sao có rủi ro.
  - *Kịch bản khai thác*: (bắt buộc cho finding bảo mật) ai làm được gì, bằng cách nào. Nếu chưa chắc chắn → hạ xuống `Thấp` và ghi "cần xác nhận thêm".
  - *Gợi ý sửa*: [Chỉ viết snippet ngắn hoặc text mô tả giải pháp].
  - *Impact Analysis*: Đánh giá rủi ro ảnh hưởng đến logic hoặc các object liên quan khi áp dụng gợi ý này.

### 2.b Đã xem xét — không phải lỗi (ĐÃ XEM XÉT)
*(Các điểm đã kiểm tra và kết luận an toàn, giữ lại kèm 1 dòng lý do — không xóa im lặng, để reviewer sau biết đã được cân nhắc. Không có mục nào thì ghi "Không có".)*
- **[Mã/Tên điểm]**: lý do kết luận an toàn.

## 3. Tối Ưu Hiệu Năng (Performance Optimization)
*(Chỉ ra các đoạn code làm chậm hệ thống và gợi ý cấu trúc dữ liệu/SQL tốt hơn)*
- **[Vấn đề Hiệu Năng]**: Tên method/đoạn code.
  - *Vấn đề*: (Vd: SELECT trong LOOP).
  - *Gợi ý sửa*: [Cách viết JOIN, FOR ALL ENTRIES hoặc dùng CDS].
  - *Impact Analysis*: Cảnh báo nếu việc tối ưu (ví dụ đổi cấu trúc data) có thể làm break code ở nơi khác đang gọi đến.

## 4. Bảo Trì & Mở Rộng (Maintainability & Clean ABAP)
- Đánh giá naming convention, độ dài hàm.
- Gợi ý sử dụng các class chuẩn SAP.

[OUTPUT FORMAT]
- All chat progress narration throughout this workflow uses `[Skill: caveman]` style per `sap-dev-rule.md` §10 — short, evidence-based, narration only (the saved report content and any code excerpts stay verbatim). This is read-only/advisory; avoid "chắc là/should be" language per `sap-dev-rule.md` §8.
- Provide the clickable link to the generated Code Review Report.
