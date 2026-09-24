#!/usr/bin/env bash
# Phase 2 self-verify helper (create-report / create-transactional-app). READ-ONLY: every call is an HTTP GET.
# Host, client and cookie file come from .mcp.json (server env SAP_URL / SAP_CLIENT / SAP_COOKIE_FILE) —
# no connection data is hardcoded here.
#
# Usage (run from the workspace root):
#   fetch.sh samecode <TYPE> <NAME>                  compare active source md5 between write + read-only server
#                                                    TYPE: DDLS | DDLX | BDEF | CLAS | SRVD
#   fetch.sh srvurl   <server> <SRVB>                print the OData V4 service URL of a published UI binding
#   fetch.sh metadata <server> <SRVB> <outdir>       save $metadata to <outdir>/metadata_<server>.xml
#   fetch.sh sample   <server> <SRVB> <EntitySet> '<query options>'
#                                                    e.g. '$filter=CompanyCode eq '"'"'1000'"'"'&$select=A,B&$top=20'
#                                                    prints total count + per-column fill ratio — NEVER the values
#                                                    (business data stays out of chat, see .claude/exceptions/)
# <server> = MCP server name, e.g. sap_gm2_cus_ro (client 100, has data-read auth) or sap_cloud_dev (080: 0 rows, no data auth)
set -uo pipefail
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../../.." && pwd)}"
mcp="$root/.mcp.json"
command -v jq >/dev/null || { echo "ERROR: jq not found" >&2; exit 2; }
[ -f "$mcp" ] || { echo "ERROR: $mcp not found" >&2; exit 2; }
syscfg="$root/.claude/common/system-config.md"
write_srv="$(grep -m1 '^WRITE_SERVERS=' "$syscfg" | cut -d= -f2 | cut -d, -f1)"
ro_srv="$(grep -m1 '^READONLY_SERVERS=' "$syscfg" | cut -d= -f2 | cut -d, -f1)"

conn() {  # $1 = server → sets URL, COOKIE
  URL="$(jq -r --arg s "$1" '.mcpServers[$s].env.SAP_URL // empty' "$mcp")"
  COOKIE="$(jq -r --arg s "$1" '.mcpServers[$s].env.SAP_COOKIE_FILE // empty' "$mcp")"
  [ -n "$URL" ] && [ -f "$COOKIE" ] || { echo "ERROR: server '$1' has no SAP_URL/cookie in .mcp.json" >&2; exit 2; }
}
get() { curl -s -b "$COOKIE" "$@"; }

srvurl() {  # $1 server, $2 SRVB
  conn "$1"
  local u; u="$(get -H 'Accept: application/vnd.sap.adt.businessservices.odatav4.v2+xml, application/vnd.sap.adt.businessservices.odatav4.v1+xml, application/xml' \
    "$URL/sap/bc/adt/businessservices/odatav4/$2?servicename=$2&serviceversion=0001&srvdname=$2" | grep -oE 'serviceUrl="[^"]+"' | head -1 | cut -d'"' -f2)"
  [ -n "$u" ] || { echo "ERROR: no serviceUrl for $2 on $1 (binding not published / SRVD name differs / cookie expired)" >&2; exit 1; }
  echo "$URL$u"
}

case "${1:-}" in
  samecode)
    t="$2"; n="$(echo "$3" | tr 'A-Z' 'a-z')"
    case "$t" in
      DDLS) p="ddic/ddl/sources/$n/source/main" ;;
      DDLX) p="ddic/ddlx/sources/$n/source/main" ;;
      BDEF) p="bo/behaviordefinitions/$n/source/main" ;;
      CLAS) p="oo/classes/$n/source/main" ;;
      SRVD) p="ddic/srvd/sources/$n/source/main" ;;
      *) echo "ERROR: TYPE must be DDLS|DDLX|BDEF|CLAS|SRVD" >&2; exit 2 ;;
    esac
    out=""
    for s in "$write_srv" "$ro_srv"; do
      conn "$s"; tmp="$(mktemp)"; code="$(get -o "$tmp" -w '%{http_code}' "$URL/sap/bc/adt/$p")"
      h="$( [ "$code" = 200 ] && md5sum < "$tmp" | cut -c1-32 || echo "http$code")"; rm -f "$tmp"
      echo "$t $3 @ $s: $h"; out="$out $h"
    done
    set -- $out; [ "$1" = "$2" ] && [ "${1#http}" = "$1" ] && echo "SAME" || { echo "DIFFERENT"; exit 1; } ;;
  srvurl)   srvurl "$2" "$3" ;;
  metadata)
    su="$(srvurl "$2" "$3")" || exit 1; mkdir -p "$4"; conn "$2"
    f="$4/metadata_$2.xml"; code="$(get -o "$f" -w '%{http_code}' "$su\$metadata")"
    echo "metadata http=$code bytes=$(wc -c < "$f") -> $f"; [ "$code" = 200 ] ;;
  sample)
    su="$(srvurl "$2" "$3")" || exit 1; conn "$2"
    q="$5"; case "$q" in *'$count'*) ;; *) q="$q&\$count=true" ;; esac
    q="$(echo "$q" | sed "s/ /%20/g; s/'/%27/g")"
    get -H 'Accept: application/json' "$su$4?$q" | node -e '
      let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{
        let d; try{d=JSON.parse(s)}catch(e){console.log("ERROR non-JSON response:",s.slice(0,200));process.exit(1)}
        if(d.error){console.log("ERROR",d.error.code,d.error.message);process.exit(1)}
        const rows=d.value||[]; console.log("total="+d["@odata.count"]+" returned="+rows.length);
        const cols=[...new Set(rows.flatMap(r=>Object.keys(r)))].filter(k=>!k.startsWith("@")&&!k.startsWith("__")&&k!=="SAP__Messages");
        for(const c of cols){const f=rows.filter(r=>r[c]!==null&&r[c]!==""&&r[c]!==undefined).length;
          console.log("  "+c.padEnd(32)+"filled "+f+"/"+rows.length+(f===0&&rows.length?"  <-- EMPTY in every row":""));}
      })' ;;
  *) sed -n '2,16p' "$0"; exit 2 ;;
esac
