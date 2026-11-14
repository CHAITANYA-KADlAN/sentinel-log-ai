G = "background:linear-gradient(145deg,var(--g1),var(--g2));backdrop-filter:blur(26px) saturate(1.8);-webkit-backdrop-filter:blur(26px) saturate(1.8);border:1px solid var(--gb);box-shadow:inset 0 1px 0 var(--hi),0 12px 40px var(--sh)"

DARK = "--bg:#000;--fg:#fff;--mut:rgba(255,255,255,.64);--g1:rgba(255,255,255,.14);--g2:rgba(255,255,255,.04);--gb:rgba(255,255,255,.2);--hi:rgba(255,255,255,.35);--sh:rgba(0,0,0,.55);--hov:rgba(255,255,255,.1);--bowl:#000;--core:rgba(255,255,255,.95);--line:rgba(255,255,255,.035)"
LIGHT = "--bg:#F4F1EF;--fg:#150A0C;--mut:rgba(21,10,12,.64);--g1:rgba(255,255,255,.8);--g2:rgba(255,255,255,.35);--gb:rgba(21,10,12,.12);--hi:rgba(255,255,255,.95);--sh:rgba(150,40,50,.2);--hov:rgba(21,10,12,.07);--bowl:#F4F1EF;--core:rgba(255,140,140,.9);--line:rgba(21,10,12,.045)"

BASE = """
<style>
:root{--red:#FF2D45;--red2:#FF6A5C;ROOT}
html,body,.stApp{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Inter","Helvetica Neue",sans-serif;color:var(--fg)}
.stApp{background-color:var(--bg)!important;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:80px 80px}
.stApp:before{content:"";position:fixed;inset:-6% -12% 0;z-index:0;pointer-events:none;background:radial-gradient(ellipse 78% 74% at 50% -6%,var(--bowl) 0 56%,var(--core) 60%,rgba(255,60,75,.95) 66%,rgba(190,10,35,.55) 75%,rgba(120,0,20,.18) 84%,transparent 92%);filter:blur(5px);opacity:GLOW;animation:breathe 8s ease-in-out infinite alternate}
[data-testid="stAppViewContainer"]{position:relative;z-index:1}[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:transparent!important}
#MainMenu,footer,header[data-testid="stHeader"],[data-testid="stSidebarHeader"],[data-testid="stSidebarCollapseButton"],[data-testid="stExpandSidebarButton"],[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"]{display:none!important}
.block-container{padding-top:96px;max-width:1120px}
iframe[height="0"]{position:absolute;width:0;height:0;border:0}[data-testid="stElementContainer"]:has(iframe[height="0"]){position:absolute;height:0;overflow:hidden;margin:0}
h1,h2,h3,h4{letter-spacing:-.02em}
.stApp :is(p,label,li,h2,h3,h4,h5,[data-testid="stMarkdownContainer"],[data-testid="stCaptionContainer"],[data-testid="stWidgetLabel"]):not(button *){color:var(--fg)!important}
.stApp :is(.sub p,.fc p,.legal p,.fhead p){color:var(--mut)!important}
/* top glass bar */
.topbar{position:fixed;top:14px;left:18px;right:18px;height:58px;z-index:1000;border-radius:32px;display:flex;align-items:center;padding:0 1.7rem;justify-content:space-between;GLASS}
.topbar:before{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(100deg,rgba(255,255,255,.18),transparent 30%,transparent 70%,rgba(255,255,255,.14));pointer-events:none}
.logo{font-weight:900;font-size:.8rem;letter-spacing:.32em;transform:scaleX(1.18);transform-origin:left;color:var(--fg);text-shadow:0 0 14px rgba(255,45,70,.7)}
.tabs{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:flex;gap:.3rem}
.tabs button{background:none;border:none;color:var(--fg);padding:.45rem 1.25rem;border-radius:99px;font:500 .92rem -apple-system,BlinkMacSystemFont,"SF Pro Display",sans-serif;cursor:pointer;transition:background .3s,color .3s}
.tabs button:hover{background:var(--hov)}.tabs button.on{background:var(--fg);color:var(--bg)}
.gearwrap{position:relative;margin-left:auto}.gear{width:40px;height:40px;border-radius:50%;cursor:pointer;color:var(--fg);font-size:1.1rem;GLASS;transition:box-shadow .3s}.gear:hover{box-shadow:0 0 24px rgba(255,45,70,.5)}
.menu{position:absolute;right:0;top:52px;min-width:200px;padding:.4rem;border-radius:20px;display:none;GLASS}.gearwrap.open .menu{display:block}
.menu button{display:block;width:100%;text-align:left;background:none;border:none;color:var(--fg);padding:.6rem .9rem;border-radius:12px;cursor:pointer;font:inherit}.menu button:hover{background:var(--hov)}
.st-key-hid{position:fixed;left:-9999px;top:0;width:240px;height:10px;overflow:hidden;opacity:0;pointer-events:none}
/* hero */
.hero5{height:calc(100vh - 150px);min-height:520px;display:grid;grid-template-rows:1fr auto;justify-items:center;padding-top:40px}
.ttlbox{width:100%}
.big{margin:0 0 0 calc(50% - 47vw);width:94vw;text-align:center;font-weight:900;font-size:7vw;line-height:1;letter-spacing:.08em;white-space:nowrap;color:var(--fg);text-shadow:0 0 26px rgba(255,45,70,.75),0 0 90px rgba(255,20,45,.5)}.big span{display:inline-block;animation:flick 6s ease-in-out infinite alternate}
.sub{text-align:center;max-width:720px;padding-bottom:1.2rem}.sub h2{font-size:2rem;font-weight:600;margin:0 0 .6rem}.sub p{line-height:1.6;margin:0}
.st-key-cta{margin-bottom:1rem}.st-key-cta .stButton>button{background:var(--fg)!important;color:var(--bg)!important;border:none;box-shadow:0 0 30px rgba(255,45,70,.35)}
.pill-red{display:block;text-align:center;padding:.62rem 1.2rem;border-radius:99px;background:linear-gradient(145deg,rgba(255,45,70,.6),rgba(110,0,20,.6));border:1px solid rgba(255,100,110,.55);color:#fff!important;text-decoration:none;box-shadow:0 0 30px rgba(255,40,60,.4);transition:.3s}.pill-red:hover{transform:translateY(-2px);box-shadow:0 0 44px rgba(255,40,60,.65)}
/* glass surfaces */
.card,.fc,.inc,.panel-h,.legal,.stButton>button,.stDownloadButton>button,[data-testid="stDataFrame"],[data-testid="stSidebar"],[data-testid="stAlert"]{GLASS;border-radius:22px}
.stButton>button,.stDownloadButton>button{color:var(--fg);padding:.65rem 1.6rem;font-weight:500;border-radius:99px!important;transition:transform .3s,box-shadow .3s}.stApp button p{color:inherit!important}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:inset 0 1px 0 var(--hi),0 0 34px rgba(255,45,70,.5);border-color:rgba(255,90,100,.7)}
.panel-h{display:flex;align-items:center;gap:.7rem;padding:.7rem 1.2rem;margin:1.8rem 0 .8rem;border-radius:99px;font-weight:600;font-size:1.05rem;width:fit-content}
.panel-h i{width:8px;height:8px;border-radius:50%;background:var(--red);box-shadow:0 0 10px var(--red)}.panel-h em{font-style:normal;font-weight:400;color:var(--mut);font-size:.9rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem}.fc{padding:1.1rem 1.3rem}.fc b{display:block;margin-bottom:.35rem}.fc p{margin:0;line-height:1.55;font-size:.93rem}.fc .n{color:var(--red);font:700 .8rem ui-monospace,Menlo,monospace}
.legal{padding:.9rem 1.3rem;margin:.6rem 0}.legal summary{cursor:pointer;font-weight:600}.legal p{margin:.6rem 0 0;line-height:1.55;font-size:.9rem}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:.5rem 0 1.4rem}.card{padding:1.1rem 1.3rem}.kpi small{color:var(--mut)}.kpi b{display:block;font-size:2rem;font-weight:600;margin-top:.2rem}.kpi.bad b{color:var(--red)}
.inc{padding:1rem 1.2rem;margin:.9rem 0 .4rem;background:linear-gradient(100deg,rgba(255,45,70,.32),var(--g2) 55%)!important}
.inc code{font:500 .9rem ui-monospace,"SF Mono",Menlo,monospace;color:var(--fg);background:none;word-break:break-all}
.meta{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.6rem;font:400 .78rem ui-monospace,"SF Mono",Menlo,monospace;color:var(--mut)}
.chip{border:1px solid var(--gb);border-radius:99px;padding:.15rem .65rem;background:var(--hov)}.sev-Critical{color:var(--red)}.sev-High{color:#FFA24D}.sev-Medium,.sev-Low{color:var(--mut)}
.tri{border-left:2px solid var(--red);padding:.3rem 0 .3rem 1rem;margin:0 0 1rem 1rem;line-height:1.55}.tri small{color:var(--mut);display:block;margin-top:.3rem}
.off{padding:1rem 1.3rem}.off .row{display:grid;grid-template-columns:150px 1fr 40px;gap:1rem;align-items:center;padding:.35rem 0;font:500 .85rem ui-monospace,"SF Mono",Menlo,monospace}.bar{height:8px;border-radius:8px;background:var(--hov)}.bar i{display:block;height:100%;border-radius:8px;background:linear-gradient(90deg,#FF8A5C,var(--red),#B0001E)}
[data-testid="stDataFrame"]{padding:2px}
[data-baseweb="select"]>div,[data-testid="stFileUploaderDropzone"]{background:var(--hov)!important;border:1px solid var(--gb)!important;border-radius:14px!important}
/* detection core: 2-D radar <-> 3-D heat map */
.fhead{display:flex;align-items:center;gap:1.4rem;margin-bottom:.5rem}.fhead h2{margin:0 0 .3rem}.fhead p{margin:0}
.dcore{position:relative;flex:none;width:130px;aspect-ratio:1;border-radius:50%;overflow:hidden;border:1px solid var(--gb);background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.2),rgba(255,45,70,.12) 60%,transparent);box-shadow:0 0 50px rgba(255,45,70,.4)}
.r2{position:absolute;inset:0;border-radius:50%;background:repeating-radial-gradient(circle,transparent 0 22%,rgba(255,120,120,.4) 22.5% 23.2%),linear-gradient(rgba(255,120,120,.4),rgba(255,120,120,.4)) center/1px 100% no-repeat,linear-gradient(rgba(255,120,120,.4),rgba(255,120,120,.4)) center/100% 1px no-repeat;transition:opacity .9s,transform .9s}
.r2:before{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,45,70,.85),rgba(255,45,70,0) 24%);animation:sweep 4.2s linear infinite}
.r3{position:absolute;inset:0;width:100%;height:100%;opacity:0;transform:scale(.8);transition:opacity .9s,transform .9s}.dcore.m3 .r2{opacity:0;transform:scale(1.15) rotate(40deg)}.dcore.m3 .r3{opacity:1;transform:none}
.blip{position:absolute;width:9%;aspect-ratio:1;border-radius:50%;background:#fff;box-shadow:0 0 14px var(--red);opacity:0;animation:blip 4.2s infinite}
/* floating, auto-minimising sidebar */
[data-testid="stSidebar"]{position:fixed!important;left:18px!important;top:96px!important;transform:none!important;margin:0!important;min-width:0!important;height:auto!important;visibility:visible!important;z-index:998;border-radius:29px;overflow:hidden;width:176px!important;max-height:58px;transition:max-height .6s cubic-bezier(.2,.8,.2,1),width .6s cubic-bezier(.2,.8,.2,1)}
[data-testid="stSidebar"].sb-open{width:320px!important;max-height:min(78vh,720px);overflow-y:auto}
[data-testid="stSidebarContent"],[data-testid="stSidebarUserContent"]{background:transparent!important;height:auto!important}[data-testid="stSidebarUserContent"]{padding:0 1.2rem 1.2rem!important}
.sb-tab{cursor:grab;touch-action:none;user-select:none;height:58px;display:flex;align-items:center;gap:.6rem;font-weight:600;white-space:nowrap}.sb-tab i{width:9px;height:9px;border-radius:50%;background:var(--red);box-shadow:0 0 10px var(--red)}
@keyframes sweep{to{transform:rotate(360deg)}}@keyframes breathe{to{transform:scale(1.04) translateY(1%)}}
@keyframes flick{0%,92%{opacity:1}95%{opacity:.82}100%{opacity:1}}@keyframes blip{0%,12%{opacity:0;transform:scale(.4)}20%{opacity:1;transform:scale(1.2)}60%{opacity:.2}100%{opacity:0}}
@media(max-width:800px){.kpis{grid-template-columns:1fr 1fr}.logo{display:none}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
"""


def css(light: bool = False, dim: bool = False) -> str:
    return BASE.replace("ROOT", LIGHT if light else DARK).replace("GLOW", ".5" if dim else "1").replace("GLASS", G)


KEYS = {"Home": "bt_home", "Features": "bt_features", "Specs / Info": "bt_specs"}


def topbar(tab: str, light: bool, tabs: list) -> str:
    btns = "".join(f'<button type="button" data-act="{KEYS[t]}"' + (' class="on"' if t == tab else "") + f">{t}</button>" for t in tabs)
    mode = "Switch to dark mode" if light else "Switch to light mode"
    return ('<div class="topbar"><span class="logo">SENTINEL LOG AI</span><nav class="tabs">' + btns + '</nav><div class="gearwrap">'
            '<button type="button" class="gear" data-menu>⚙</button><div class="menu"><button type="button" data-act="bt_theme">' + mode +
            '</button><button type="button" data-act="bt_reset">Reset logs</button></div></div></div>')


JS = """<script>
(function(){var P=window.parent,D=P.document;if(P.__sl6)return;P.__sl6=1;var T=0,rf=0;
function sc(){return D.querySelector('[data-testid="stMain"]')||D.querySelector('section.main')}
var BL='.panel-h,.fc,.legal,.sub,.big,.kpi,.inc,.tri,.off,.fhead,[data-testid="stVegaLiteChart"],[data-testid="stArrowVegaLiteChart"],[data-testid="stDownloadButton"],.st-key-cta,[data-testid="stAlert"]';
var calm=P.matchMedia&&P.matchMedia('(prefers-reduced-motion: reduce)').matches;
function barrel(){rf=0;var els=D.querySelectorAll(BL),vh=P.innerHeight,R=vh*.85,rs=[],i,f,a;
for(i=0;i<els.length;i++){els[i].style.transform='';if(calm)els[i].style.opacity=''}if(calm)return;
for(i=0;i<els.length;i++){var r=els[i].getBoundingClientRect();rs.push((r.top+r.bottom)/2)}
for(i=0;i<els.length;i++){f=Math.max(-1,Math.min(1,(rs[i]-vh*.5)/R));a=Math.abs(f);els[i].style.transform='perspective(1200px) translateZ('+(-a*260).toFixed(1)+'px) rotateX('+(-f*38).toFixed(2)+'deg)';els[i].style.opacity=(1-.7*a*a).toFixed(3)}}
function sched(){if(!rf){rf=1;P.requestAnimationFrame(barrel)}}
function fitT(){var s=D.querySelector('.big span');if(!s||s.__w===P.innerWidth)return;s.__w=P.innerWidth;var h=s.parentNode;h.style.transform='';h.style.fontSize='100px';h.style.fontSize=(100*P.innerWidth*.94/s.getBoundingClientRect().width)+'px'}
var C=[[30,0,8],[150,10,30],[255,55,70],[255,225,200]];
function col(h){h=Math.max(0,Math.min(.999,h))*3;var i=h|0,f=h-i,a=C[i],b=C[i+1];return 'rgb('+[0,1,2].map(function(k){return Math.round(a[k]+(b[k]-a[k])*f)}).join(',')+')'}
function H(i,j,t){return .5+.28*Math.sin(i*.55+t)+.22*Math.cos(j*.6-t*.8)+.35*Math.exp(-(Math.pow(i-7-4*Math.sin(t*.7),2)+Math.pow(j-7-4*Math.cos(t*.5),2))/10)}
function heat(){var r=D.querySelector('.dcore');if(!r||r.querySelector('canvas'))return;var c=D.createElement('canvas');c.className='r3';c.width=c.height=320;r.appendChild(c);P.setInterval(function(){r.classList.toggle('m3')},7000)}
function draw(){var c=D.querySelector('canvas.r3');if(c&&c.parentNode.classList.contains('m3')){var x=c.getContext('2d'),W=c.width,N=15,t=(T+=.02),a=t*.35,ca=Math.cos(a),sa=Math.sin(a),q=[];x.clearRect(0,0,W,W);
for(var i=0;i<N-1;i++)for(var j=0;j<N-1;j++){q.push([[0,0],[1,0],[1,1],[0,1]].map(function(o){var X=i+o[0]-7,Z=j+o[1]-7,h=H(i+o[0],j+o[1],t),rx=X*ca-Z*sa,rz=X*sa+Z*ca;return [W/2+(rx-rz)*10.5,W*.62+(rx+rz)*5.2-h*58,h,rx+rz]}))}
q.sort(function(u,v){return u[0][3]-v[0][3]});q.forEach(function(cs){var h=(cs[0][2]+cs[2][2])/2;x.beginPath();cs.forEach(function(p,k){k?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1])});x.closePath();x.fillStyle=col((h-.1)/1.2);x.fill();x.strokeStyle='rgba(255,255,255,.2)';x.lineWidth=.8;x.stroke()})}
P.requestAnimationFrame(draw)}
draw();
D.addEventListener('click',function(e){var g=D.querySelector('.gearwrap'),b=e.target.closest('[data-act]');
if(b){var h=D.querySelector('.st-key-'+b.getAttribute('data-act')+' button');h&&h.click();g&&g.classList.remove('open');return}
if(e.target.closest('[data-menu]')){g&&g.classList.toggle('open');return}
if(g&&!e.target.closest('.menu'))g.classList.remove('open');
if(e.target.closest('.pill-red')){e.preventDefault();var t=D.getElementById('learn');t&&t.scrollIntoView({behavior:'smooth'})}});
function side(){var sb=D.querySelector('[data-testid="stSidebar"]');if(!sb||sb.__s)return;sb.__s=1;var t,mv=0,ox=0,oy=0;
function fit(){var r=sb.getBoundingClientRect(),w=320,h=Math.min(P.innerHeight*.78,720);sb.style.setProperty('left',Math.max(8,Math.min(r.left,P.innerWidth-w-8))+'px','important');sb.style.setProperty('top',Math.max(8,Math.min(r.top,P.innerHeight-h-8))+'px','important')}
function open(){clearTimeout(t);if(!sb.classList.contains('sb-open')){fit();sb.classList.add('sb-open')}}
function shut(){var a=D.activeElement;if(a&&sb.contains(a))a.blur();sb.classList.remove('sb-open')}
function later(){clearTimeout(t);t=setTimeout(function(){if(mv||D.querySelector('[role="listbox"]'))later();else shut()},900)}
sb.addEventListener('mouseenter',open);sb.addEventListener('mouseleave',later);sb.addEventListener('focusin',open);
D.addEventListener('mousedown',function(e){if(!sb.contains(e.target)&&!e.target.closest('[role="listbox"]'))later()});
sb.addEventListener('pointerdown',function(e){var h=e.target.closest('.sb-tab');if(!h)return;var r=sb.getBoundingClientRect();ox=e.clientX-r.left;oy=e.clientY-r.top;mv=1;h.setPointerCapture(e.pointerId);e.preventDefault()});
sb.addEventListener('pointermove',function(e){if(!mv)return;sb.style.setProperty('left',Math.max(0,Math.min(P.innerWidth-176,e.clientX-ox))+'px','important');sb.style.setProperty('top',Math.max(0,Math.min(P.innerHeight-58,e.clientY-oy))+'px','important')});
sb.addEventListener('pointerup',function(){if(mv){mv=0;fit()}});
sb.classList.add('sb-open');t=setTimeout(shut,2800)}
function scan(){var s=sc();if(s&&!s.__b){s.__b=1;s.addEventListener('scroll',sched,{passive:true})}heat();side();fitT();sched()}
var q=0;new P.MutationObserver(function(){if(!q){q=1;P.requestAnimationFrame(function(){q=0;scan()})}}).observe(D.body,{childList:true,subtree:true});
P.addEventListener('scroll',sched,{passive:true});P.addEventListener('resize',function(){var s=D.querySelector('.big span');if(s)s.__w=0;scan()});scan();})();
</script>"""
