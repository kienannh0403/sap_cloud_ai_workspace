#!/usr/bin/env node
// Phase 2.U helper — dump what a Fiori Elements app will actually receive from an OData V4 $metadata:
// per entity type: LineItem, SelectionFields, mandatory filters, HeaderInfo, Facets, FieldGroups, default sort,
// and per property: Label, Text/TextArrangement, value help, Hidden, mandatory, currency/unit reference.
// This is the "actual" side of the UI checklist; the "expected" side is the spec (TS §2/§4/§7 + fs_markdown.md).
// Items metadata cannot prove (rendering, F4 returning rows, formatting) are NOT covered — they go to Phase 2.M.
//
// Usage: node ui-check.js <metadata.xml> [--ddlx <ddlx_source.txt> ...]
//   --ddlx : also scan metadata-extension source for duplicate @UI positions (positions are not in $metadata).
'use strict';
const fs = require('fs');
const args = process.argv.slice(2);
if (!args.length) { console.error('usage: node ui-check.js <metadata.xml> [--ddlx <file> ...]'); process.exit(2); }
const ddlx = []; let metaFile;
for (let i = 0; i < args.length; i++) args[i] === '--ddlx' ? ddlx.push(args[++i]) : (metaFile = args[i]);

// ---- minimal XML → tree (enough for EDMX: no DTD, no CDATA in practice) ----
function parse(xml) {
  const root = { tag: '#root', attr: {}, kids: [], text: '' }; const st = [root];
  const re = /<(\/?)([\w:.]+)((?:\s+[\w:.]+="[^"]*")*)\s*(\/?)>|([^<]+)/g; let m;
  while ((m = re.exec(xml))) {
    if (m[5] !== undefined) { st[st.length - 1].text += m[5].trim(); continue; }
    if (m[1]) { st.pop(); continue; }
    const attr = {}; for (const a of m[3].matchAll(/([\w:.]+)="([^"]*)"/g)) attr[a[1]] = a[2];
    const n = { tag: m[2].replace(/^.*:/, ''), attr, kids: [], text: '' };
    st[st.length - 1].kids.push(n); if (!m[4]) st.push(n);
  }
  return root;
}
const all = (n, tag, out = []) => { for (const k of n.kids) { if (k.tag === tag) out.push(k); all(k, tag, out); } return out; };
const kids = (n, tag) => n.kids.filter(k => k.tag === tag);
const short = s => (s || '').replace(/\(.*$/, '').replace(/^.*\./, '');
// value of an Annotation / PropertyValue node, rendered compactly
function val(n) {
  for (const k of ['String', 'Path', 'PropertyPath', 'AnnotationPath', 'EnumMember', 'Bool', 'Int', 'Decimal', 'NavigationPropertyPath'])
    if (n.attr[k] !== undefined) return k === 'EnumMember' ? short(n.attr[k].split(' ')[0].replace(/\/.*$/, '')) + '/' + n.attr[k].replace(/^.*\//, '') : n.attr[k];
  const c = kids(n, 'Collection')[0]; if (c) return c.kids.map(v => v.tag === 'Record' ? rec(v) : (v.text || val(v)));
  const r = kids(n, 'Record')[0]; if (r) return rec(r);
  return n.text || true;
}
function rec(r) {
  const o = { $type: short(r.attr.Type || '') };
  for (const p of kids(r, 'PropertyValue')) o[p.attr.Property] = val(p);
  for (const a of kids(r, 'Annotation')) o['@' + short(a.attr.Term)] = val(a);
  return o;
}

const x = parse(fs.readFileSync(metaFile, 'utf8'));
const types = {}; // typeName -> {props:{name:type}, key:[]}
for (const s of all(x, 'Schema')) for (const et of kids(s, 'EntityType'))
  types[et.attr.Name] = { props: Object.fromEntries(kids(et, 'Property').map(p => [p.attr.Name, p.attr.Type])),
    nav: kids(et, 'NavigationProperty').map(p => p.attr.Name), key: all(et, 'PropertyRef').map(p => p.attr.Name) };
const sets = all(x, 'EntitySet').map(s => ({ name: s.attr.Name, type: short(s.attr.EntityType) }));

// annotations indexed by target: "Type" / "Type/Prop" / "Container/Set"
const ann = {};
for (const a of all(x, 'Annotations')) {
  const tgt = a.attr.Target.replace(/^[\w.]+\./, '');
  for (const t of kids(a, 'Annotation')) {
    const k = short(t.attr.Term) + (t.attr.Qualifier ? '#' + t.attr.Qualifier : '');
    (ann[tgt] = ann[tgt] || {})[k] = val(t);
  }
}
const A = (t) => ann[t] || {};
const warn = [];
const hiddenProp = (T, p) => A(`${T}/${p}`).Hidden !== undefined;

for (const { name: set, type: T } of sets) {
  const ty = types[T]; if (!ty) continue;
  const ta = A(T); const ca = A(`Container/${set}`);
  if (!ta.LineItem && !ta.SelectionFields && !ta.Facets && !ta.HeaderInfo) continue; // not a UI-relevant entity
  console.log(`\n=== EntitySet ${set}  (type ${T}, key: ${ty.key.join(', ')})`);
  if (ta.HeaderInfo) console.log('HeaderInfo:', JSON.stringify(ta.HeaderInfo));

  const li = ta.LineItem || [];
  console.log(`LineItem (${li.length}, metadata order):`);
  li.forEach((r, i) => {
    const f = r.Value, lab = r.Label || (f && A(`${T}/${f}`).Label);
    console.log(`  ${String(i + 1).padStart(2)}. ${r.$type.padEnd(22)} ${(f || short(r.Action)).padEnd(28)} label="${lab || ''}"${r['@Importance'] ? ' importance=' + r['@Importance'] : ''}`);
    if (f && !lab) warn.push(`${set}: line item column ${f} has no label`);
  });

  const sf = ta.SelectionFields || [];
  const req = ((ca.FilterRestrictions || {}).RequiredProperties) || [];
  const nonFilt = ((ca.FilterRestrictions || {}).NonFilterableProperties) || [];
  console.log(`SelectionFields (${sf.length}):`);
  for (const f of sf) {
    const pa = A(`${T}/${f}`), vh = pa.ValueListReferences || pa.ValueList || pa.ValueListMapping;
    const vhName = Array.isArray(vh) ? vh.map(u => (String(u).match(/srvd_f4\/sap\/([^/]+)/) || [])[1] || (u.CollectionPath || '?')).join(',') : (vh ? (vh.CollectionPath || 'yes') : '');
    console.log(`  - ${f.padEnd(28)} ${ty.props[f] || '?'} label="${pa.Label || ''}" mandatory=${req.includes(f) ? 'Y' : '-'} valuehelp=${vhName || '-'}${pa.ValueListWithFixedValues ? ' (dropdown)' : ''}`);
    if (!vh && !/Date|Time|Boolean/.test(ty.props[f] || '')) warn.push(`${set}: selection field ${f} has no value help`);
    if (nonFilt.includes(f)) warn.push(`${set}: selection field ${f} is marked NonFilterable`);
    if (!ty.props[f]) warn.push(`${set}: selection field ${f} is not a property of ${T}`);
  }
  if (req.length) console.log('Mandatory filters (FilterRestrictions.RequiredProperties):', req.join(', '));
  for (const k of Object.keys(ta).filter(k => /^(PresentationVariant|SelectionPresentationVariant|SelectionVariant)/.test(k)))
    console.log(`${k}:`, JSON.stringify(ta[k]));
  if (ta.Facets) console.log('Facets:', JSON.stringify(ta.Facets));
  for (const k of Object.keys(ta).filter(k => /^(FieldGroup|Identification)/.test(k)))
    console.log(`${k}:`, (ta[k].Data || ta[k]).map ? (ta[k].Data || ta[k]).map(r => r.Value || short(r.Action)).join(', ') : JSON.stringify(ta[k]));

  console.log('Properties:');
  const shown = new Set([...li.map(r => r.Value), ...sf].filter(Boolean));
  for (const [p, t] of Object.entries(ty.props)) {
    if (p.startsWith('__') || p === 'SAP__Messages') continue;
    const pa = A(`${T}/${p}`);
    const flags = [pa.Hidden !== undefined && 'hidden', pa.HiddenFilter !== undefined && 'hiddenFilter',
      pa.Text && `text=${pa.Text}${pa['TextArrangement'] ? '(' + pa.TextArrangement + ')' : ''}`,
      pa.ISOCurrency && `currency=${pa.ISOCurrency}`, pa.Unit && `unit=${pa.Unit}`,
      pa.FieldControl && `fieldControl=${pa.FieldControl}`, shown.has(p) && 'ON-SCREEN'].filter(Boolean);
    console.log(`  ${p.padEnd(28)} ${t.replace(/^Edm\./, '').padEnd(16)} label="${pa.Label || ''}" ${flags.join(' ')}`);
    if (shown.has(p) && !pa.Label) warn.push(`${set}: on-screen field ${p} has no label`);
    if (/Decimal/.test(t) && shown.has(p) && !pa.ISOCurrency && !pa.Unit) warn.push(`${set}: numeric field ${p} on screen without currency/unit reference — check it is meant to be a plain number`);
    const vh = pa.ValueListReferences || pa.ValueList;
    if (vh && shown.has(p) && !pa.Text) warn.push(`${set}: ${p} has a value help (code field?) but no Common.Text — screen shows the code only`);
    if (shown.has(p) && hiddenProp(T, p)) warn.push(`${set}: ${p} is both on screen and UI.Hidden`);
  }
}

// ---- duplicate @UI positions from DDLX source (positions are dropped from $metadata) ----
for (const f of ddlx) {
  const src = fs.readFileSync(f, 'utf8').replace(/\/\/.*$/gm, '');
  const seen = {};
  // split into element blocks: annotations ... elementName;
  for (const blk of src.split(/;\s*(?=@|\}|$)/)) {
    const el = (blk.match(/(\w+)\s*$/) || [])[1]; if (!el) continue;
    for (const m of blk.matchAll(/@UI\.(lineItem|selectionField|identification|fieldGroup)\s*:\s*\[([\s\S]*?)\]\s*(?=@|\w+\s*$)/g))
      for (const r of m[2].matchAll(/\{([^{}]*)\}/g)) {
        if (/type\s*:\s*#FOR_ACTION|#FOR_INTENT_BASED/.test(r[1])) continue;
        const pos = (r[1].match(/position\s*:\s*(\d+)/) || [])[1]; if (!pos) continue;
        const q = (r[1].match(/qualifier\s*:\s*'([^']+)'/) || [])[1] || '';
        const k = `${m[1]}${q ? '#' + q : ''} position ${pos}`; (seen[k] = seen[k] || []).push(el);
      }
  }
  for (const [k, els] of Object.entries(seen)) if (els.length > 1) warn.push(`DDLX ${f.replace(/^.*[\\/]/, '')}: ${k} used by ${els.join(' + ')} — display order between them is undefined`);
}

console.log(`\n=== WARNINGS (${warn.length}) — hints only; the verdict per checklist line comes from comparing with the spec`);
for (const w of warn) console.log('  ! ' + w);
