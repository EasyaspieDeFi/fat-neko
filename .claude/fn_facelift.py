#!/usr/bin/env python3
# Fat Neko facelift v3 — self-correcting: strips any prior fn-facelift block, re-injects corrected one.
import re, sys
P = '/Users/lucy/dev/fat-neko/index.html'
h = open(P, encoding='utf-8').read()

# Remove any previously injected blocks (idempotent / re-runnable).
h = re.sub(r'\n?<style id="fn-facelift">.*?</style>', '', h, flags=re.S)
h = re.sub(r'\n?<script id="fn-facelift-js">.*?</script>', '', h, flags=re.S)

BLOCK = r"""
<style id="fn-facelift">
/* ===================== FAT NEKO · FACELIFT LAYER ===================== */
:root{ --fn-mint:#6fe9cb; --fn-edge:rgba(255,255,255,.07); }
html{ -webkit-tap-highlight-color:transparent; }

/* Ambient aurora behind the existing dot grid */
body{ background:
    radial-gradient(60% 42% at 18% -4%, rgba(111,233,203,.12), transparent 60%),
    radial-gradient(55% 40% at 100% 4%, rgba(182,156,242,.12), transparent 60%),
    radial-gradient(80% 55% at 50% 108%, rgba(94,200,255,.07), transparent 60%),
    #04080a !important; }

/* Cards: gradient fill + crisp top highlight */
.card{ background:linear-gradient(180deg,#15271f,#0c1814) !important; border-color:#0a201a !important;
  box-shadow:0 5px 0 #00120e, 0 16px 30px -14px rgba(0,0,0,.75), inset 0 1px 0 rgba(255,255,255,.06) !important; }

/* Top bar: single-row glass with refined chips (no more 2-row wrap) */
.topbar{ gap:5px !important; padding:9px 9px !important; flex-wrap:nowrap !important; align-items:center;
  overflow:hidden;
  background:linear-gradient(180deg, rgba(10,22,18,.86), rgba(5,12,10,.66)) !important;
  -webkit-backdrop-filter:blur(16px) saturate(160%); backdrop-filter:blur(16px) saturate(160%);
  border-bottom:1px solid var(--fn-edge) !important; }
.topbar .chip{ flex:0 0 auto; gap:5px !important; padding:6px 9px !important; border-radius:11px !important;
  font-size:11.5px !important; font-weight:800 !important; line-height:1 !important;
  border:1px solid var(--fn-edge) !important;
  background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.018)) !important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06), 0 6px 14px -10px rgba(0,0,0,.85) !important;
  transition:transform .1s ease, border-color .2s ease, background .2s ease; }
.topbar .chip:active{ transform:translateY(1px) scale(.97); }
.topbar .chip:hover{ border-color:var(--fn-edge2); }
.topbar .chip .ic{ font-size:0 !important; display:flex; align-items:center; }
.topbar .chip svg{ width:15px; height:15px; display:block; flex:0 0 auto; }
.topbar .chip span{ line-height:1; }
.topbar .chip.bal{ color:var(--fn-mint) !important;
  background:linear-gradient(180deg, rgba(111,233,203,.16), rgba(111,233,203,.05)) !important;
  border-color:rgba(111,233,203,.30) !important; }
.topbar .chip.bal svg{ color:var(--fn-mint); }
.topbar .chip.fn-burn svg{ color:#ff9a52; }
.topbar .chip.fn-mute{ padding:6px 7px !important; }
.topbar .chip.fn-mute svg{ color:#9fb6ad; }
.topbar .chip.fn-new svg{ color:#ffd05e; }
.topup{ flex:0 0 auto; margin-left:auto !important; padding:7px 11px !important; border-radius:11px !important;
  border:0 !important; font-weight:800 !important; letter-spacing:0; font-size:11.5px !important; white-space:nowrap;
  background:linear-gradient(180deg,#ffe07a,#ffc63a) !important; color:#3a2a00 !important;
  box-shadow:0 8px 18px -8px rgba(255,200,60,.6), inset 0 1px 0 rgba(255,255,255,.55) !important;
  transition:transform .1s ease, box-shadow .1s ease; }
.topup:active{ transform:translateY(2px); box-shadow:0 3px 8px -4px rgba(255,200,60,.55) !important; }

/* Tab bar: glass + custom SVG icons + active glow */
.tabbar{ background:linear-gradient(180deg, rgba(8,18,15,.72), rgba(4,10,8,.92)) !important;
  -webkit-backdrop-filter:blur(20px) saturate(160%); backdrop-filter:blur(20px) saturate(160%);
  border-top:1px solid var(--fn-edge) !important;
  box-shadow:0 -10px 30px -16px rgba(0,0,0,.8), inset 0 1px 0 rgba(255,255,255,.05) !important; }
.tabbar .tab{ position:relative; transition:color .2s, transform .16s cubic-bezier(.2,.9,.3,1.3); }
.tabbar .tab:active{ transform:scale(.9); }
.tabbar .tab .ti{ display:flex; align-items:center; justify-content:center; min-height:24px; }
.tabbar .tab .ti[data-fn="1"]{ font-size:0; }   /* hide emoji only once the SVG is in (graceful fallback) */
.tabbar .tab .ti svg{ width:24px; height:24px; display:block; transition:transform .26s cubic-bezier(.2,.9,.3,1.5); }
.tabbar .tab.on{ color:var(--fn-mint) !important;
  background:linear-gradient(180deg, rgba(111,233,203,.16), rgba(111,233,203,.04)) !important;
  box-shadow:inset 0 0 0 1px rgba(111,233,203,.24) !important; }
.tabbar .tab.on .ti svg{ transform:translateY(-1px) scale(1.1); filter:drop-shadow(0 3px 7px rgba(111,233,203,.55)); }
.tabbar .tab.on::before{ content:""; position:absolute; top:2px; left:50%; transform:translateX(-50%);
  width:16px; height:3px; border-radius:3px; background:var(--fn-mint); box-shadow:0 0 9px rgba(111,233,203,.85); }

/* Buttons: gradient sheen + inset highlight (keeps press-down feel) */
.btn{ box-shadow:0 4px 0 #00120e, inset 0 1px 0 rgba(255,255,255,.22) !important; }
.btn.mint{ background:linear-gradient(180deg,#8af3da,#4fd6b6) !important; }
.btn.blue{ background:linear-gradient(180deg,#86d6ff,#4bb6f0) !important; }
.btn.gold{ background:linear-gradient(180deg,#ffe07a,#ffcb3f) !important; }
.btn.pink{ background:linear-gradient(180deg,#c6acff,#a888f0) !important; }
.btn.ghost{ background:linear-gradient(180deg,#1a3128,#12241d) !important; border-color:#0a201a !important; }
.buy{ background:linear-gradient(180deg,#8af3da,#4fd6b6) !important;
  box-shadow:0 4px 0 #00120e, inset 0 1px 0 rgba(255,255,255,.3) !important; transition:transform .1s, box-shadow .1s; }

/* Mood bar: glossy gradient + shimmer */
.mbar{ box-shadow:inset 0 2px 4px rgba(0,0,0,.45) !important; }
.mbar>i{ position:relative; overflow:hidden; box-shadow:inset 0 1px 0 rgba(255,255,255,.3); }
.mbar>i::after{ content:""; position:absolute; inset:0;
  background:linear-gradient(90deg, transparent, rgba(255,255,255,.45), transparent);
  transform:translateX(-100%); animation:fn-shimmer 2.6s cubic-bezier(.4,0,.2,1) infinite; }
@keyframes fn-shimmer{ 0%{transform:translateX(-100%)} 60%,100%{transform:translateX(220%)} }

/* Pet stage: soft spotlight behind the canvas */
.stage{ background:
    radial-gradient(70% 55% at 50% 42%, rgba(111,233,203,.14), transparent 70%),
    radial-gradient(120% 100% at 50% 0%, #16302a, #08130f) !important;
  box-shadow:inset 0 0 0 2px rgba(255,255,255,.08), inset 0 -16px 30px -16px rgba(0,0,0,.7) !important; }

/* Speech bubble + chat */
.bubble{ box-shadow:0 6px 0 #00120e, 0 12px 22px -12px rgba(0,0,0,.6) !important; }
.msg{ box-shadow:0 2px 8px -3px rgba(0,0,0,.4) !important; }
.msg.you{ background:linear-gradient(180deg,#8af3da,#5fdcbc) !important; }
.msg.neko{ background:linear-gradient(180deg,#1a3128,#12241d) !important; border:1px solid var(--fn-edge); }
.chatbar input{ transition:border-color .2s, box-shadow .2s; }
.chatbar input:focus, .keyrow input:focus, .keyrow select:focus{ outline:none !important;
  border-color:var(--fn-mint) !important; box-shadow:0 0 0 3px rgba(111,233,203,.16) !important; }
.qchip{ transition:transform .1s, box-shadow .1s, border-color .2s; }
.qchip:hover{ border-color:rgba(111,233,203,.4); }

/* List items / stats / tickers */
.item{ background:linear-gradient(180deg,#18302a,#12241d) !important; border-color:#0a201a !important; }
.stat{ background:linear-gradient(180deg,#18302a,#12241d) !important; box-shadow:inset 0 1px 0 rgba(255,255,255,.05); }
.lbrow.you{ box-shadow:0 0 14px -4px rgba(111,233,203,.5); }
.pmt, .fng{ background:linear-gradient(180deg,#16302a,#0e1c17) !important; border-color:#0a201a !important;
  box-shadow:0 3px 0 #00120e, inset 0 1px 0 rgba(255,255,255,.05) !important; }

/* Modal depth */
.modal{ background:linear-gradient(180deg,#16302a,#0d1a16) !important;
  box-shadow:0 5px 0 #00120e, 0 30px 60px -20px rgba(0,0,0,.9), inset 0 1px 0 rgba(255,255,255,.07) !important; }

/* Custom scrollbars */
*::-webkit-scrollbar{ width:7px; height:7px; }
*::-webkit-scrollbar-thumb{ background:rgba(111,233,203,.22); border-radius:8px; }
*::-webkit-scrollbar-thumb:hover{ background:rgba(111,233,203,.4); }
*::-webkit-scrollbar-track{ background:transparent; }

@media (prefers-reduced-motion:reduce){ .mbar>i::after{ animation:none; } }
</style>
<script id="fn-facelift-js">
(function(){
  "use strict";
  var CAT  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5c.67 0 1.35.09 2 .26 1.78-2 5.03-2.84 6.42-2.26 1.4.58-.42 7-.42 7 .57 1.07 1 2.24 1 3.44C21 17.9 16.97 21 12 21s-9-3-9-7.56c0-1.25.5-2.4 1-3.44 0 0-1.89-6.42-.5-7 1.39-.58 4.72.23 6.5 2.23A9.04 9.04 0 0 1 12 5Z"/><path d="M8 14v.5"/><path d="M16 14v.5"/><path d="M11.25 16.25h1.5L12 17l-.75-.75Z"/></svg>';
  var BOWL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21a9 9 0 0 0 9-9H3a9 9 0 0 0 9 9Z"/><path d="M7 21h10"/><path d="M19.5 12 22 6"/><path d="M16.25 3c.27.1.8.53.75 1.36-.06.83-.93 1.2-1 2.02-.05.78.34 1.24.73 1.62"/><path d="M11.25 3c.27.1.8.53.74 1.36-.05.83-.93 1.2-.98 2.02-.06.78.33 1.24.72 1.62"/><path d="M6.25 3c.27.1.8.53.75 1.36-.06.83-.93 1.2-1 2.02-.05.78.34 1.24.74 1.62"/></svg>';
  var CHART= '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><rect x="7" y="11" width="3" height="6" rx="1"/><rect x="12" y="7" width="3" height="10" rx="1"/><rect x="17" y="13" width="3" height="4" rx="1"/></svg>';
  var BOT  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>';
  // Map by label text so icon assignment is independent of tab order. Falls back per-index.
  var BY_LABEL = { neko:CAT, feed:BOWL, profile:CHART, agent:BOT };
  var FALLBACK = [CAT, BOWL, CHART, BOT];
  function iconFor(tab, i){
    var spans = tab.querySelectorAll('span');
    var label = (spans.length>1 ? spans[spans.length-1].textContent : '').trim().toLowerCase();
    return BY_LABEL[label] || FALLBACK[i] || null;
  }
  var painting=false;
  function paint(){
    if(painting) return;
    var bar=document.getElementById('tabbar'); if(!bar) return;
    var tabs=bar.querySelectorAll('.tab'); if(!tabs.length) return;
    painting=true;
    try{
      for(var i=0;i<tabs.length;i++){
        var ti=tabs[i].querySelector('.ti'); var svg=iconFor(tabs[i], i);
        if(ti && svg && ti.getAttribute('data-fn')!=='1'){ ti.innerHTML=svg; ti.setAttribute('data-fn','1'); }
      }
    } finally { painting=false; }
  }
  // --- Top-bar chip icons (coin / flame / volume / egg), swapped in place of emoji ---
  var COIN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M14.6 9.4A2.7 2.7 0 0 0 12 7.8c-1.6 0-2.8.9-2.8 2.2 0 3 5.6 1.5 5.6 4.5 0 1.3-1.2 2.2-2.8 2.2a2.7 2.7 0 0 1-2.6-1.6"/><path d="M12 6.2v1.6"/><path d="M12 16.2v1.6"/></svg>';
  var FLAME='<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2c.5 3-2 4.5-3.3 6.2C7.2 10 6.5 11.7 6.5 13.6a5.5 5.5 0 0 0 11 0c0-1.7-.7-3.3-1.8-4.7-.3 1.1-1 1.8-1.9 2.1.6-2.2-.2-4.6-1.8-6.3C11.2 3.8 12 2.9 12 2Z"/></svg>';
  var VON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M16 9a4 4 0 0 1 0 6"/><path d="M19 7a8 8 0 0 1 0 10"/></svg>';
  var VOFF='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4z"/><line x1="22" y1="9" x2="16" y2="15"/><line x1="16" y1="9" x2="22" y2="15"/></svg>';
  var EGG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c3.3 0 6 4.4 6 9a6 6 0 0 1-12 0c0-4.6 2.7-9 6-9Z"/></svg>';
  var ptop=false;
  function paintTop(){
    if(ptop) return;
    var bar=document.getElementById('topbar'); if(!bar) return;
    var chips=bar.querySelectorAll('.chip'); if(!chips.length) return;
    ptop=true;
    try{
      for(var i=0;i<chips.length;i++){
        var chip=chips[i];
        if(chip.getAttribute('data-fn')==='1') continue;
        var html=chip.innerHTML, hit=false;
        if(html.indexOf('🪙')>=0){ html=html.replace('🪙',COIN); hit=true; }                 /* coin */
        if(html.indexOf('🔥')>=0){ html=html.replace('🔥',FLAME); chip.classList.add('fn-burn'); hit=true; } /* flame */
        if(html.indexOf('🔇')>=0){ html=html.replace('🔇',VOFF); chip.classList.add('fn-mute'); hit=true; }  /* mute */
        else if(html.indexOf('🔈')>=0){ html=html.replace('🔈',VON); chip.classList.add('fn-mute'); hit=true; } /* sound */
        if(html.indexOf('🥚')>=0){ html=html.replace('🥚',EGG); chip.classList.add('fn-new'); hit=true; }   /* egg */
        if(hit){ chip.innerHTML=html; }
        chip.setAttribute('data-fn','1');
      }
    } finally { ptop=false; }
  }
  function repaint(){ paint(); paintTop(); }
  function start(){
    var tb=document.getElementById('tabbar');
    if(tb){ try{ new MutationObserver(paint).observe(tb,{childList:true,subtree:true}); }catch(e){} }
    var top=document.getElementById('topbar');
    if(top){ try{ new MutationObserver(paintTop).observe(top,{childList:true,subtree:true}); }catch(e){} }
    repaint();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start); else start();
  setTimeout(repaint,200); setTimeout(repaint,800); setTimeout(repaint,2000);
})();
</script>
"""

if h.count('</body>') != 1:
    sys.stderr.write('UNEXPECTED </body> count: %d\n' % h.count('</body>')); sys.exit(1)
h = h.replace('</body>', BLOCK + '</body>')
open(P, 'w', encoding='utf-8').write(h)
# self-verify
h2 = open(P, encoding='utf-8').read()
ok = ('id="fn-facelift"' in h2) and ('id="fn-facelift-js"' in h2) and (h2.count('viewBox="0 0 24 24"')>=4) and (h2.count('</body>')==1)
print('APPLIED' if ok else 'VERIFY_FAILED', 'bytes=%d' % len(h2))
sys.exit(0 if ok else 3)
