G = "background:linear-gradient(145deg,rgba(255,255,255,.2),rgba(255,255,255,.06));backdrop-filter:blur(26px) saturate(1.9);-webkit-backdrop-filter:blur(26px) saturate(1.9);border:1px solid rgba(255,255,255,.26);box-shadow:inset 0 1px 0 rgba(255,255,255,.5),inset 0 -1px 0 rgba(255,255,255,.08),0 12px 40px rgba(6,12,50,.38)"

CSS = """
<style>
:root{--p:0;--R0:min(42vh,360px);--T0:clamp(46px,7.4vw,96px);--cy:#7BE4FF;--rd:#FF6B8B;--am:#FFC46B;--tx:#F2F6FF;--mut:rgba(220,230,255,.62)}
html,body,.stApp{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Inter","Helvetica Neue",sans-serif;color:var(--tx)}
.stApp{background:#0D1636}
.stApp:before{content:"";position:fixed;inset:-25%;pointer-events:none;background:radial-gradient(48vmax 40vmax at 18% 22%,rgba(64,132,255,.62),transparent 62%),radial-gradient(42vmax 36vmax at 82% 14%,rgba(176,92,255,.5),transparent 62%),radial-gradient(46vmax 38vmax at 72% 88%,rgba(20,214,200,.42),transparent 62%),radial-gradient(38vmax 32vmax at 8% 86%,rgba(255,96,150,.34),transparent 62%);animation:drift 30s ease-in-out infinite alternate}
[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:transparent!important}
#MainMenu,footer,[data-testid="stSidebarHeader"],[data-testid="stSidebarCollapseButton"],[data-testid="stExpandSidebarButton"],[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"]{display:none!important}
header[data-testid="stHeader"]{background:transparent}
.block-container{padding-top:0;max-width:1120px}
iframe[height="0"]{position:absolute;width:0;height:0;border:0}
[data-testid="stElementContainer"]:has(iframe[height="0"]){position:absolute;height:0;overflow:hidden;margin:0}
h1,h2,h3,h4{letter-spacing:-.02em}
/* ---------- hero stage: big -> docked bar, driven by --p (0..1) ---------- */
.stage{position:fixed;z-index:999;pointer-events:none;top:calc(12px*var(--p));left:calc(16px*var(--p));right:calc(16px*var(--p));height:calc(100vh - (100vh - 68px)*var(--p))}
.stage:before{content:"";position:absolute;inset:0;border-radius:calc(34px*var(--p));opacity:var(--p);GLASS}
.radar{position:absolute;aspect-ratio:1;width:calc(var(--R0) - (var(--R0) - 40px)*var(--p));top:calc(36% + 14%*var(--p));left:calc(50% - (50% - 40px)*var(--p));transform:translate(-50%,-50%);border-radius:50%;border:1px solid rgba(255,255,255,.5);background:repeating-radial-gradient(circle,transparent 0 22%,rgba(255,255,255,.28) 22.5% 23.2%),linear-gradient(rgba(255,255,255,.28),rgba(255,255,255,.28)) center/1px 100% no-repeat,linear-gradient(rgba(255,255,255,.28),rgba(255,255,255,.28)) center/100% 1px no-repeat,radial-gradient(circle at 35% 30%,rgba(255,255,255,.28),rgba(123,228,255,.1) 60%,transparent);backdrop-filter:blur(10px);box-shadow:inset 0 2px 0 rgba(255,255,255,.55),0 0 calc(70px*(1 - var(--p))) rgba(123,228,255,.45)}
.radar:before{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(123,228,255,.75),rgba(123,228,255,0) 24%);animation:sweep 4.2s linear infinite}
.blip{position:absolute;width:9%;aspect-ratio:1;border-radius:50%;background:var(--rd);box-shadow:0 0 14px var(--rd);opacity:0;animation:blip 4.2s infinite}
.ttl{position:absolute;white-space:nowrap;top:calc(36% + 14%*var(--p) + (var(--R0)/2 + 62px)*(1 - var(--p)));left:calc(50% - (50% - 76px)*var(--p));transform:translate(calc(-50%*(1 - var(--p))),-50%)}
.ttl h1{margin:0;line-height:1;font-weight:700;font-size:calc(var(--T0) - (var(--T0) - 21px)*var(--p));background:linear-gradient(120deg,#fff 30%,#BFEFFF);-webkit-background-clip:text;color:transparent}
.ttl p{position:absolute;top:100%;left:50%;transform:translateX(-50%);width:min(520px,86vw);white-space:normal;text-align:center;margin:1rem 0 0;color:var(--mut);font-size:1.05rem;line-height:1.5;opacity:calc(1 - var(--p)*3)}
.cue{position:absolute;bottom:4vh;left:50%;transform:translateX(-50%);color:var(--mut);font-size:.85rem;opacity:calc(1 - var(--p)*5);animation:bob 2.2s ease-in-out infinite}
.spacer{height:calc(100vh - 10px)}
/* ---------- glass surfaces ---------- */
.card,.inc,.panel-h,.stButton>button,.stDownloadButton>button,[data-testid="stDataFrame"],[data-testid="stSidebar"],[data-testid="stAlert"]{GLASS;border-radius:22px}
.panel-h{display:flex;align-items:center;gap:.7rem;padding:.7rem 1.2rem;margin:1.8rem 0 .8rem;border-radius:99px;font-weight:600;font-size:1.05rem;width:fit-content}
.panel-h i{width:8px;height:8px;border-radius:50%;background:var(--cy);box-shadow:0 0 10px var(--cy)}.panel-h em{font-style:normal;font-weight:400;color:var(--mut);font-size:.9rem}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:.5rem 0 1.4rem}
.card{padding:1.1rem 1.3rem}.kpi small{color:var(--mut)}.kpi b{display:block;font-size:2rem;font-weight:600;margin-top:.2rem}.kpi.bad b{color:var(--rd)}
.inc{padding:1rem 1.2rem;margin:.9rem 0 .4rem;background:linear-gradient(100deg,rgba(255,100,130,.3),rgba(255,255,255,.08) 55%)!important}
.inc code{font:500 .9rem ui-monospace,"SF Mono",Menlo,monospace;color:#fff;background:none;word-break:break-all}
.meta{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.6rem;font:400 .78rem ui-monospace,"SF Mono",Menlo,monospace;color:var(--mut)}
.chip{border:1px solid rgba(255,255,255,.22);border-radius:99px;padding:.15rem .65rem;background:rgba(255,255,255,.08)}
.sev-Critical{color:var(--rd)}.sev-High{color:var(--am)}.sev-Medium,.sev-Low{color:var(--cy)}
.tri{border-left:2px solid var(--cy);padding:.3rem 0 .3rem 1rem;margin:0 0 1rem 1rem;line-height:1.55}.tri small{color:var(--mut);display:block;margin-top:.3rem}
.stButton>button,.stDownloadButton>button{color:#fff;padding:.7rem 1.7rem;font-weight:500;border-radius:99px;transition:transform .3s,box-shadow .3s}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px) scale(1.02);box-shadow:inset 0 1px 0 rgba(255,255,255,.6),0 0 34px rgba(123,228,255,.5);border-color:rgba(255,255,255,.6);color:#fff}
[data-testid="stDataFrame"]{overflow:hidden;padding:2px}
[data-baseweb="select"]>div,[data-testid="stFileUploaderDropzone"]{background:rgba(255,255,255,.1)!important;border:1px solid rgba(255,255,255,.22)!important;border-radius:14px!important}
/* ---------- floating, auto-minimising sidebar ---------- */
[data-testid="stSidebar"]{position:fixed!important;left:18px!important;top:96px!important;transform:none!important;margin:0!important;min-width:0!important;height:auto!important;visibility:visible!important;z-index:998;border-radius:29px;overflow:hidden;width:176px!important;max-height:58px;transition:max-height .6s cubic-bezier(.2,.8,.2,1),width .6s cubic-bezier(.2,.8,.2,1)}
[data-testid="stSidebar"].sb-open{width:320px!important;max-height:min(78vh,720px);overflow-y:auto}
[data-testid="stSidebarContent"],[data-testid="stSidebarUserContent"]{background:transparent!important;height:auto!important}
[data-testid="stSidebarUserContent"]{padding:0 1.2rem 1.2rem!important}
.sb-tab{height:58px;display:flex;align-items:center;gap:.6rem;font-weight:600;white-space:nowrap}.sb-tab i{width:9px;height:9px;border-radius:50%;background:var(--cy);box-shadow:0 0 10px var(--cy)}
/* ---------- scroll-reactive reveal (class added by JS) ---------- */
.rv{opacity:0;transform:translateY(calc(var(--dir,1)*46px)) scale(.965);filter:blur(8px);transition:opacity .7s cubic-bezier(.2,.8,.2,1),transform .8s cubic-bezier(.2,.8,.2,1),filter .7s;transition-delay:calc(var(--i,0)*70ms)}
.rv.in{opacity:1;transform:none;filter:none}
@keyframes sweep{to{transform:rotate(360deg)}}@keyframes bob{50%{transform:translate(-50%,6px)}}
@keyframes drift{to{transform:translate3d(4%,3%,0) scale(1.08) rotate(3deg)}}
@keyframes blip{0%,12%{opacity:0;transform:scale(.4)}20%{opacity:1;transform:scale(1.2)}60%{opacity:.2}100%{opacity:0}}
@media(max-width:800px){.kpis{grid-template-columns:1fr 1fr}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.rv{opacity:1;transform:none;filter:none}}
</style>
""".replace("GLASS", G)

HERO = """<div class="stage"><div class="radar"><span class="blip" style="top:20%;left:62%;animation-delay:.6s"></span><span class="blip" style="top:64%;left:26%;animation-delay:2.4s"></span><span class="blip" style="top:42%;left:16%;animation-delay:3.4s"></span></div><div class="ttl"><h1>SentinelLog AI</h1><p>Isolation-forest anomaly detection and signature matching for server logs, with plain-English triage for the analyst on shift.</p></div><div class="cue">Scroll to begin</div></div><div class="spacer"></div>"""

JS = """<script>
(function(){var P=window.parent,D=P.document;if(P.__sl)return;P.__sl=1;var R=D.documentElement,last=0;
function sc(){return D.querySelector('[data-testid="stMain"]')||D.querySelector('section.main')}
function onS(){var s=sc(),y=s?s.scrollTop:(P.scrollY||0);R.style.setProperty('--p',Math.min(1,Math.max(0,y/(P.innerHeight*.55))).toFixed(4));
if(Math.abs(y-last)>2){R.style.setProperty('--dir',y>last?1:-1);last=y}}
var SEL='.panel-h,[data-testid="stDataFrame"],.kpi,.inc,.tri,[data-testid="stVegaLiteChart"],[data-testid="stArrowVegaLiteChart"],[data-testid="stDownloadButton"]';
var io=new P.IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('in',e.isIntersecting)})},{threshold:.1,rootMargin:'0px 0px -5% 0px'});
function scan(){var s=sc();if(s&&!s.__b){s.__b=1;s.addEventListener('scroll',onS,{passive:true})}
D.querySelectorAll(SEL).forEach(function(el,i){if(!el.__o){el.__o=1;el.style.setProperty('--i',i%4);el.classList.add('rv');io.observe(el)}});
var sb=D.querySelector('[data-testid="stSidebar"]');if(sb&&!sb.__s){sb.__s=1;var t;
function shut(){var a=D.activeElement;if(a&&sb.contains(a))a.blur();sb.classList.remove('sb-open')}
function later(){clearTimeout(t);t=setTimeout(function(){D.querySelector('[data-baseweb="popover"]')?later():shut()},1000)}
sb.addEventListener('mouseenter',function(){clearTimeout(t);sb.classList.add('sb-open')});
sb.addEventListener('mouseleave',later);sb.addEventListener('focusin',function(){clearTimeout(t);sb.classList.add('sb-open')});
D.addEventListener('mousedown',function(e){if(!sb.contains(e.target)&&!e.target.closest('[data-baseweb="popover"]'))later()});
sb.classList.add('sb-open');t=setTimeout(shut,2800)}}
var q=0;new P.MutationObserver(function(){if(!q){q=1;P.requestAnimationFrame(function(){q=0;scan()})}}).observe(D.body,{childList:true,subtree:true});
P.addEventListener('scroll',onS,{passive:true});scan();onS();})();
</script>"""
