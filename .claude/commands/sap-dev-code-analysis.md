---
description: Sử dụng workflow này khi có yêu cầu đọc, phân tích sâu và xuất báo cáo tài liệu chi tiết cho một hoặc một nhóm đối tượng/package trên hệ thống SAP.
argument-hint: <object-or-package-name> [analysis-focus]
---

> **Claude Code note:** `[Skill: X]` below means invoke the `x` skill via the Skill tool (auto-discovered from `.claude/skills/x/`).

[ROLE & OBJECTIVE]
Act as an Expert SAP System Architect & Technical Analyst. Your task is to extract, read, and comprehensively analyze a given SAP Object or Package using the system's MCP tools, and then produce a detailed technical documentation report.

[INPUT DATA]
- Target: [Tên Object, Danh sách Object, hoặc Tên Package]
- Analysis Focus: [Ví dụ: Tìm hiểu luồng data, Phân tích nghiệp vụ, Vẽ data model, Phân tích Call Graph...]
- Additional Requirements: [Các yêu cầu khác từ user]
- Arguments: $ARGUMENTS

[EXECUTION PROTOCOL - CRITICAL]
Since analyzing a whole package or complex object might produce an excessive amount of text, you MUST follow this chunking protocol:
1. SCAN: Always list the structure first. Do NOT attempt to read all source codes at once.
2. FILTER: Identify the core components (Main classes, Root CDS Views, Key Tables).
3. DEEP DIVE: Read the source code of only the filtered core components to understand the business logic and relationships.
4. DOCUMENT: Synthesize the findings into a structured markdown report.

[STEP-BY-STEP INSTRUCTIONS]
Please execute the following sequence:

Step 0: System Scanning & Component Discovery
Required Skill: [Skill: scratchpad]
Action:
- If `artifacts/targets/[Target]/` already exists: [Skill: target-refresh] steps 1–3 first (read-only: report any change made outside the workspace since the last recorded version and ask whether to record it; never open a version here).
- Use whichever MCP tool your environment exposes for reading/searching SAP objects to get the initial structure/list of objects (`sap-dev-rule.md` §9) — if it isn't loaded yet, use `ToolSearch` to find it first.
- Create `artifacts/targets/[Target]/build/scratchpad_analysis.md` (`sap-dev-rule.md` §4 — one sub-folder per target).
- Document the tree structure in the scratchpad and select the top priority objects that contain the core logic/data models.

Step 1: Deep Dive Analysis
Required Skill: [Skill: fs-logic-behavior-translator] & [Skill: fs-data-model-extractor]
Action:
- Sequentially read the source codes of the prioritized objects using the same verified MCP tool — `include_context: false`, pull each source to a file once and grep it afterwards instead of re-reading (`.claude/common/lean-sap-io.md` §2).
- Analyze:
  - Data Model: How tables and CDS views are linked (Joins, Associations).
  - Business Logic: What the main ABAP Classes/Methods do.
  - Integration: Any API calls or external interactions.
- Continuously update your findings in the scratchpad.

Step 2: Generate Final Technical Report
Action:
Create the final, comprehensive Markdown document. 
Location: `artifacts/targets/[Target]/analysis/analysis_report.md`.
Then create or update `artifacts/targets/[Target]/INDEX.md` per `sap-dev-rule.md` §4 — the short entry point (what the object is, status, open questions, blockers, file map) that later sessions read instead of this full report. Findings worth keeping beyond this report (traps, decisions, data-preview results) go to `artifacts/targets/[Target]/notes/<topic>.md`, one per file, each linked from INDEX.md.

Handbook record: create/refresh `artifacts/targets/[Target]/handbook.json` (`.claude/common/handbook-target.md`) with `purpose` and `objects` (each analysed object with its `uses`, so the page shows the object diagram) — no version is opened by an analysis (versions are versions of the report/function, opened only by a code change); an analysis of an existing target is logged in today's `records` entry — one per day, created or extended (`kind` += "phân tích", `applies_to` = the function version analysed, one `summary` line) — then run `python .claude/scripts/handbook/render_target.py [Target]`.
Format the report exactly as follows:

# [Tên Đối Tượng/Package] - System Analysis Report

## 1. Giới thiệu (Introduction)
- Mục đích của đối tượng/package này là gì?
- Thuộc phân hệ (Module) nào? Ngữ cảnh sử dụng (Business Context).

## 2. Thành phần cốt lõi (Core Components)
- Liệt kê các Tables, CDS Views, RAP Behavior, Classes, Interfaces chính yếu.
- Giải thích ngắn gọn vai trò của từng thành phần.

## 3. Mô hình Dữ liệu (Data Model)
- Phân tích chi tiết các bảng và CDS view.
- (Tùy chọn) Cung cấp sơ đồ Mermaid `mermaid erDiagram` để biểu diễn mối quan hệ (1-1, 1-n) giữa các Entity chính.

## 4. Luồng hoạt động & Chức năng (Functional & Control Flow)
- Giải thích luồng hoạt động chính (Ví dụ: Từ khi user trigger action đến khi ghi DB).
- Phân tích chi tiết logic code trong các method quan trọng.
- Xử lý lỗi (Error Handling) và Transaction control (nếu có).
- (Tùy chọn) Cung cấp sơ đồ Mermaid `mermaid sequenceDiagram` hoặc `mermaid flowchart` mô tả luồng gọi.

## 5. Tổng kết, Đánh giá & Đề xuất cải tiến (Conclusion & Recommendations)
- Đánh giá kiến trúc hiện tại (Độ phức tạp, có tuân thủ Clean Core và Best Practices không?).
- Phân tích rủi ro & Lỗi tiềm ẩn: Chỉ ra các đoạn code có nguy cơ gây lỗi (vd: không bắt try-catch, thiếu kiểm tra quyền, v.v.).
- Đề xuất tối ưu hiệu năng: Đưa ra góp ý chỉnh sửa để tối ưu hóa truy vấn DB (SQL), giảm thiểu vòng lặp, hoặc tăng cường khả năng chịu tải.
- Những điểm cần lưu ý khi bảo trì hoặc mở rộng (Extensibility) trong tương lai.

[OUTPUT FORMAT]
- All chat progress narration throughout this workflow uses `[Skill: caveman]` style per `sap-dev-rule.md` §10 — short, evidence-based, narration only (the saved report content and any code excerpts stay verbatim). This is a read-only analysis; still avoid "chắc là/should be" language per `sap-dev-rule.md` §8, cite what was actually read.
- Provide the clickable link to the generated Final Technical Report.
