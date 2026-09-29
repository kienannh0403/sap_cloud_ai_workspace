#!/usr/bin/env bash
# Stop guard for rule §8 REPORTING LANGUAGE (idea adapted from ECC delivery-gate, MIT, github.com/affaan-m/ecc):
# "Never say 'should work / probably fine / likely correct.' Every 'Activated/Passed/Correct' claim needs cited
# evidence." Scans the final assistant message of the turn for hedged-verdict phrases (English + Vietnamese) and
# blocks the stop ONCE, asking to replace each phrase with the evidence (command run, output observed) or to
# state plainly that the item is unverified.
#   - Text inside code blocks, `inline code` and "quotes" / “quotes” is ignored (quoting the rule is not a violation).
#   - stop_hook_active=true (the turn already continued once because of a Stop hook) -> pass, so it never loops.
#   - Advisory by nature: no jq / no message -> pass (fail open; the SAP guards are the hard gates, not this).
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0
input=$(cat)

[[ "$(echo "$input" | jq -r '.stop_hook_active // false')" == "true" ]] && exit 0

# Final message: last_assistant_message when the harness sends it, else the text of the last assistant turn
# (assistant entries after the last real user prompt) from the transcript tail.
msg=$(echo "$input" | jq -r '.last_assistant_message // ""')
if [[ -z "$msg" ]]; then
  tp=$(echo "$input" | jq -r '.transcript_path // ""')
  [[ -n "$tp" && -f "$tp" ]] || exit 0
  msg=$(tail -n 400 "$tp" | jq -R -s -r '
    split("\n") | map(fromjson? // empty) | map(select(.type == "user" or .type == "assistant")) as $e
    | ($e | map(.type == "user" and ((.message.content | type) == "string"
                 or ((.message.content | type) == "array" and (.message.content | any(.type == "text")))))
          | rindex(true)) as $i
    | $e[(($i // -1) + 1):] | map(select(.type == "assistant") | .message.content[]? | select(.type == "text") | .text)
    | join("\n")' 2>/dev/null)
fi
[[ -z "$msg" ]] && exit 0

# Drop quoted material before matching.
clean=$(printf '%s' "$msg" | jq -R -s -r '
  gsub("```[\\s\\S]*?```"; " ") | gsub("`[^`\\n]*`"; " ") | gsub("\"[^\"\\n]*\""; " ") | gsub("“[^”\\n]*”"; " ")')

en='should (work|be fine|be ok|be correct)|probably (fine|works?|correct|ok)|likely (correct|fine|works?|ok)|seems to work|looks (fine|good|ok) to me'
vi='chắc (là )?(chạy|ổn|đúng|được|ok)|có lẽ (là )?(đúng|ổn|chạy|được)|(nên|sẽ) ổn thôi|hẳn là (đúng|ổn|chạy)|có vẻ (đúng|ổn|chạy được)|chắc không sao'
hits=$(printf '%s' "$clean" | grep -oiE "$en|$vi" | sort -u | paste -sd ',' - | sed 's/,/, /g')
[[ -z "$hits" ]] && exit 0

echo "report-language-guard (rule §8): hedged verdict in your final message: ${hits}. Replace each with the evidence (command run + output observed) or state plainly that the item is NOT verified yet and what would verify it. Activated ≠ Correct — state both separately. If the phrase is not a verdict (e.g. you are quoting someone), put it in quotes and stop again." >&2
exit 2
