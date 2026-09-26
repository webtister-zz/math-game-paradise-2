#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成长方形和正方形 - 六合一模块选择PK游戏"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

T = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{title} - PK对战</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Microsoft YaHei',sans-serif;background:linear-gradient(180deg,#1a1a2e,#16213e,#0f3460);min-height:100vh;overflow:hidden;user-select:none;-webkit-user-select:none;color:#fff}}
.top-bar{{display:flex;align-items:center;justify-content:center;padding:8px;gap:10px;background:rgba(0,0,0,0.4);flex-wrap:wrap}}
.top-bar h1{{font-size:1.1em;background:linear-gradient(90deg,#FFD700,#6C5CE7,#4ECDC4);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.timer{{font-size:1.5em;font-weight:bold;color:#FFD700;min-width:60px;text-align:center}}
.round-info{{font-size:0.85em;color:#aaa}}
.module-badge{{font-size:0.75em;background:rgba(108,92,231,0.25);color:#a78bfa;padding:2px 10px;border-radius:10px}}
.arena{{display:flex;flex:1;height:calc(100vh - 190px)}}
.player{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:12px 8px;position:relative;overflow-y:auto;transition:all 0.3s}}
.player.left{{background:linear-gradient(180deg,rgba(255,107,107,0.15),rgba(0,0,0,0.3));border-right:3px solid #FF6B6B}}
.player.right{{background:linear-gradient(180deg,rgba(78,205,196,0.15),rgba(0,0,0,0.3));border-left:3px solid #4ECDC4}}
.player-name{{font-size:1.1em;font-weight:bold;margin-bottom:4px;display:flex;align-items:center;gap:6px}}
.left .player-name{{color:#FF6B6B}}
.right .player-name{{color:#4ECDC4}}
.player-score{{font-size:2em;font-weight:bold;margin:4px 0}}
.left .player-score{{color:#FF6B6B}}
.right .player-score{{color:#4ECDC4}}
.streak{{font-size:0.8em;color:#FFD700;min-height:20px}}
.question-box{{background:rgba(255,255,255,0.1);border-radius:14px;padding:14px 10px;margin:6px 0;width:100%;text-align:center;min-height:60px;display:flex;align-items:center;justify-content:center;font-size:1.05em;line-height:1.4;flex-direction:column;overflow-x:auto}}
.diagram{{font-family:'Courier New',monospace;font-size:0.95em;line-height:1.4;display:inline-block;background:rgba(0,0,0,0.2);padding:6px 10px;border-radius:8px;margin:4px 0;white-space:pre;color:#FFD700}}
.options-grid{{display:grid;grid-template-columns:1fr 1fr;gap:6px;width:100%;margin:6px 0}}
.p-opt{{padding:10px 6px;border-radius:12px;border:2px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.05);color:#fff;font-size:0.85em;font-weight:bold;cursor:pointer;transition:all 0.2s;font-family:inherit;text-align:center;line-height:1.3;min-height:44px;display:flex;align-items:center;justify-content:center}}
.p-opt:hover{{background:rgba(255,255,255,0.15);border-color:rgba(255,255,255,0.5);transform:scale(1.04)}}
.p-opt:active{{transform:scale(0.94)}}
.p-opt.correct{{background:#10B981!important;border-color:#10B981!important;animation:pop 0.4s}}
.p-opt.wrong{{background:#EF4444!important;border-color:#EF4444!important;animation:shake 0.4s}}
.p-opt:disabled{{pointer-events:none;opacity:0.5}}
.left .p-opt.correct{{box-shadow:0 0 20px rgba(255,107,107,0.6)}}
.right .p-opt.correct{{box-shadow:0 0 20px rgba(78,205,196,0.6)}}
@keyframes pop{{0%{{transform:scale(1)}}50%{{transform:scale(1.1)}}100%{{transform:scale(1)}}}}
@keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-6px)}}75%{{transform:translateX(6px)}}}}
.feedback{{font-size:0.85em;font-weight:bold;min-height:22px;text-align:center;margin:3px 0}}
.vs-badge{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:2.5em;font-weight:bold;z-index:10;text-shadow:0 0 30px rgba(255,215,0,0.8);pointer-events:none;animation:vsPulse 1.5s infinite}}
@keyframes vsPulse{{0%,100%{{opacity:0.6;transform:translate(-50%,-50%)scale(1)}}50%{{opacity:1;transform:translate(-50%,-50%)scale(1.1)}}}}
.bottom-bar{{display:flex;align-items:center;justify-content:center;gap:16px;padding:8px;background:rgba(0,0,0,0.5);flex-wrap:wrap}}
.module-bar{{display:flex;align-items:center;justify-content:center;gap:6px;padding:6px 8px;background:rgba(0,0,0,0.3);flex-wrap:wrap}}
.mod-btn{{padding:8px 12px;border-radius:16px;border:2px solid rgba(255,255,255,0.25);background:rgba(255,255,255,0.05);color:#ccc;font-size:0.75em;font-weight:bold;cursor:pointer;font-family:inherit;transition:all 0.2s;white-space:nowrap;line-height:1.3}}
.mod-btn:hover{{border-color:rgba(255,255,255,0.5);background:rgba(255,255,255,0.1);color:#fff}}
.mod-btn.active{{border-color:#a78bfa!important;background:rgba(108,92,231,0.25)!important;color:#a78bfa!important;box-shadow:0 0 12px rgba(108,92,231,0.35)}}
.ctrl-btn{{padding:10px 22px;border-radius:20px;border:none;font-size:0.9em;font-weight:bold;cursor:pointer;font-family:inherit;transition:all 0.2s}}
.ctrl-btn.start{{background:linear-gradient(135deg,#FFD700,#FF9800);color:#333}}
.ctrl-btn.restart{{background:linear-gradient(135deg,#FF6B6B,#ee5a5a);color:#fff}}
.ctrl-btn.music{{background:rgba(255,255,255,0.1);color:#fff;border:1px solid rgba(255,255,255,0.3)}}
.ctrl-btn:hover{{transform:translateY(-2px);box-shadow:0 4px 15px rgba(0,0,0,0.3)}}
.win-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:100;display:none;align-items:center;justify-content:center;flex-direction:column}}
.win-overlay.show{{display:flex}}
.win-title{{font-size:2.5em;font-weight:bold;margin-bottom:10px;animation:bounceIn 0.6s}}
.win-subtitle{{font-size:1.2em;color:#ccc;margin-bottom:20px}}
.win-scores{{display:flex;gap:40px;margin-bottom:20px}}
.win-player{{text-align:center}}
.win-player .wscore{{font-size:3em;font-weight:bold}}
.win-player.left-w .wscore{{color:#FF6B6B}}
.win-player.right-w .wscore{{color:#4ECDC4}}
@keyframes bounceIn{{0%{{transform:scale(0.3);opacity:0}}50%{{transform:scale(1.1)}}100%{{transform:scale(1);opacity:1}}}}
.confetti{{position:fixed;pointer-events:none;z-index:101;animation:fall linear forwards}}
@keyframes fall{{0%{{transform:translateY(-100px)rotate(0);opacity:1}}100%{{transform:translateY(105vh)rotate(720deg);opacity:0}}}}
@media(max-width:600px){{
  .arena{{flex-direction:column;height:auto}}
  .player.left{{border-right:none;border-bottom:3px solid #FF6B6B}}
  .player.right{{border-left:none;border-top:3px solid #4ECDC4}}
  .player{{padding:8px 6px}}
  .question-box{{font-size:0.85em;min-height:40px;padding:8px}}
  .p-opt{{font-size:0.75em;padding:8px 4px;min-height:36px}}
  .vs-badge{{font-size:1.5em;top:50%}}
  .player-score{{font-size:1.4em}}
  .win-title{{font-size:1.6em}}
  .options-grid{{gap:4px}}
  .mod-btn{{font-size:0.68em;padding:5px 8px}}
  .diagram{{font-size:0.8em}}
}}
</style>
</head>
<body>
<div class="top-bar">
  <h1>{title} ⚔️ PK对战</h1>
  <span class="module-badge" id="mdBadge">模块一</span>
  <span class="round-info">第 <span id="rn">1</span>/10 轮</span>
  <span class="timer">⏱ <span id="tm">12</span>s</span>
</div>

<div class="module-bar" id="moduleBar">
  <button class="mod-btn active" onclick="switchModule(0)">模块一<br>垂线和平行线</button>
  <button class="mod-btn" onclick="switchModule(1)">模块二<br>画垂线</button>
  <button class="mod-btn" onclick="switchModule(2)">模块三<br>点到直线距离</button>
  <button class="mod-btn" onclick="switchModule(3)">模块四<br>平行线间距离</button>
  <button class="mod-btn" onclick="switchModule(4)">模块五<br>长方形正方形特征</button>
  <button class="mod-btn" onclick="switchModule(5)">模块六<br>画长方形正方形</button>
</div>

<div class="arena">
  <div class="player left" id="p1">
    <div class="player-name">🔴 红方玩家</div>
    <div class="player-score" id="s1">0</div>
    <div class="streak" id="st1"></div>
    <div class="question-box" id="q1">选择模块后<br>点击开始对战</div>
    <div id="ansArea1"></div>
    <div class="feedback" id="fb1"></div>
  </div>
  <div class="vs-badge">⚡VS⚡</div>
  <div class="player right" id="p2">
    <div class="player-name">🔵 蓝方玩家</div>
    <div class="player-score" id="s2">0</div>
    <div class="streak" id="st2"></div>
    <div class="question-box" id="q2">选择模块后<br>点击开始对战</div>
    <div id="ansArea2"></div>
    <div class="feedback" id="fb2"></div>
  </div>
</div>

<div class="bottom-bar">
  <button class="ctrl-btn start" id="btnStart" onclick="startGame()">⚔️ 开始对战</button>
  <button class="ctrl-btn music" id="btnMusic" onclick="toggleMusic()">🔊 音乐</button>
  <button class="ctrl-btn restart" onclick="restartGame()">🔄 重新开始</button>
</div>

<div class="win-overlay" id="winOverlay">
  <div class="win-title" id="winTitle"></div>
  <div class="win-subtitle" id="winSub"></div>
  <div class="win-scores">
    <div class="win-player left-w"><div style="color:#FF6B6B">🔴 红方</div><div class="wscore" id="ws1">0</div></div>
    <div class="win-player right-w"><div style="color:#4ECDC4">🔵 蓝方</div><div class="wscore" id="ws2">0</div></div>
  </div>
  <button class="ctrl-btn restart" onclick="restartGame()" style="font-size:1.2em;padding:14px 36px">🔄 再来一局</button>
  <button class="ctrl-btn restart" onclick="backToMenu()" style="font-size:1em;padding:10px 28px;margin-top:10px;background:rgba(255,255,255,0.1);color:#fff;border:1px solid rgba(255,255,255,0.3)">📋 选择其他模块</button>
</div>

<script>
var ALL_Q = {all_questions};

var Q = [];
var curModule = 0;
var sc=[0,0],cr=0,tr=10,tm=12,ti=null,go=false,ans=[false,false];
var sk='pk_'+window.location.pathname.replace(/[^a-zA-Z0-9]/g,'_');
var musicOn=true,actx=null;

var modNames = ['模块一：判断垂线和平行线','模块二：画垂线','模块三：点到直线的距离','模块四：平行线之间的距离','模块五：长方形和正方形特征','模块六：画长方形和正方形'];

function sf(a){{var r=a.slice();for(var i=r.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=r[i];r[i]=r[j];r[j]=t;}}return r;}}

function initAudio(){{if(!actx){{actx=new(window.AudioContext||window.webkitAudioContext)();}}}}

function playTone(f,d,ty,vol){{if(!musicOn||!actx)return;try{{var o=actx.createOscillator();var g=actx.createGain();o.type=ty||'sine';o.frequency.setValueAtTime(f,actx.currentTime);g.gain.setValueAtTime(vol||0.1,actx.currentTime);g.gain.exponentialRampToValueAtTime(0.001,actx.currentTime+d);o.connect(g);g.connect(actx.destination);o.start();o.stop(actx.currentTime+d);}}catch(e){{}}}}

function sfxCorrect(){{playTone(523,0.15,'square',0.08);setTimeout(function(){{playTone(659,0.15,'square',0.08);}},100);setTimeout(function(){{playTone(784,0.2,'square',0.08);}},200);}}
function sfxWrong(){{playTone(200,0.3,'sawtooth',0.06);}}
function sfxWin(){{for(var i=0;i<5;i++){{setTimeout(function(){{playTone(523+Math.random()*500,0.2,'square',0.07);}},i*150);}}}}
function sfxTick(){{playTone(800,0.05,'sine',0.04);}}

function toggleMusic(){{initAudio();musicOn=!musicOn;document.getElementById('btnMusic').textContent=musicOn?'🔊 音乐':'🔇 静音';if(musicOn){{playTone(440,0.1,'sine',0.05);}}}}

function switchModule(idx){{if(go)return;curModule=idx;Q=ALL_Q[idx].slice();document.getElementById('mdBadge').textContent=modNames[idx].substring(0,6);var btns=document.querySelectorAll('.mod-btn');btns.forEach(function(b,i){{b.classList.toggle('active',i===idx);}});document.getElementById('q1').innerHTML='已选：'+modNames[idx]+'<br>点击开始对战';document.getElementById('q2').innerHTML='已选：'+modNames[idx]+'<br>点击开始对战';document.getElementById('ansArea1').innerHTML='';document.getElementById('ansArea2').innerHTML='';}}

function startGame(){{initAudio();if(Q.length===0){{Q=ALL_Q[curModule].slice();}}document.getElementById('btnStart').style.display='none';document.getElementById('moduleBar').style.display='none';go=true;sc=[0,0];cr=0;ans=[false,false];document.getElementById('s1').textContent='0';document.getElementById('s2').textContent='0';document.getElementById('winOverlay').classList.remove('show');Q=sf(Q);nextRound();}}

function nextRound(){{if(cr>=tr){{endGame();return;}}ans=[false,false];document.getElementById('rn').textContent=cr+1;var q=Q[cr];renderChoice(1,q);renderChoice(2,q);tm=12;document.getElementById('tm').textContent=tm;clearInterval(ti);ti=setInterval(function(){{tm--;document.getElementById('tm').textContent=tm;if(tm<=5)sfxTick();if(tm<=0){{clearInterval(ti);timeUp();}}}},1000);}}

function renderChoice(pn,q){{
  document.getElementById('fb'+pn).innerHTML='';
  document.getElementById('st'+pn).textContent='';
  var qText=q.q1||q.q;
  var opts=q.o1||q.o;
  var ansIdx=q.a1!==undefined?q.a1:q.a;
  document.getElementById('q'+pn).innerHTML='<div style="font-size:0.82em;color:#ccc;margin-bottom:3px">第'+(cr+1)+'题</div>'+qText;
  document.getElementById('q'+pn).style.display='';
  var ix=[0,1,2,3];
  for(var i=ix.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=ix[i];ix[i]=ix[j];ix[j]=t;}}
  var lb=['A','B','C','D'];
  var h='<div class="options-grid">';
  for(var i=0;i<4;i++){{
    var oi=ix[i];
    h+='<button class="p-opt" onclick="answerChoice('+pn+','+oi+','+ansIdx+',this)" id="ob'+pn+'_'+i+'">'+lb[i]+'. '+opts[oi]+'</button>';
  }}
  h+='</div>';
  document.getElementById('ansArea'+pn).innerHTML=h;
}}

function answerChoice(pn,oi,ai,btn){{
  if(!go||ans[pn-1])return;
  ans[pn-1]=true;
  var bs=document.querySelectorAll('#ansArea'+pn+' .p-opt');
  bs.forEach(function(b){{b.disabled=true;}});
  if(oi===ai){{
    btn.classList.add('correct');
    sc[pn-1]+=10;
    document.getElementById('s'+pn).textContent=sc[pn-1];
    document.getElementById('fb'+pn).innerHTML='✅ 正确！+10';
    document.getElementById('st'+pn).textContent='🔥 连击！';
    sfxCorrect();
  }}else{{
    btn.classList.add('wrong');
    document.getElementById('fb'+pn).innerHTML='❌ 答错了';
    document.getElementById('st'+pn).textContent='';
    sfxWrong();
    for(var i=0;i<bs.length;i++){{
      var lb=['A','B','C','D'];
      if(bs[i].textContent.indexOf(lb[ai]+'.')>=0)bs[i].classList.add('correct');
    }}
  }}
  if(ans[0]&&ans[1]){{clearInterval(ti);cr++;setTimeout(function(){{nextRound();}},1200);}}
}}

function timeUp(){{
  for(var p=1;p<=2;p++){{
    if(!ans[p-1]){{
      var opts=document.querySelectorAll('#ansArea'+p+' .p-opt');
      opts.forEach(function(b){{b.disabled=true;}});
      document.getElementById('fb'+p).innerHTML='⏰ 时间到！';
    }}
  }}
  cr++;setTimeout(function(){{nextRound();}},1200);
}}

function endGame(){{
  go=false;clearInterval(ti);
  document.getElementById('winOverlay').classList.add('show');
  document.getElementById('ws1').textContent=sc[0];
  document.getElementById('ws2').textContent=sc[1];
  if(sc[0]>sc[1]){{
    document.getElementById('winTitle').innerHTML='🔴 红方获胜！';
    document.getElementById('winTitle').style.color='#FF6B6B';
    document.getElementById('winSub').innerHTML=modNames[curModule]+'<br>红方 '+sc[0]+' : '+sc[1]+' 蓝方';
    sfxWin();
  }}else if(sc[1]>sc[0]){{
    document.getElementById('winTitle').innerHTML='🔵 蓝方获胜！';
    document.getElementById('winTitle').style.color='#4ECDC4';
    document.getElementById('winSub').innerHTML=modNames[curModule]+'<br>蓝方 '+sc[1]+' : '+sc[0]+' 红方';
    sfxWin();
  }}else{{
    document.getElementById('winTitle').innerHTML='🤝 平局！';
    document.getElementById('winTitle').style.color='#FFD700';
    document.getElementById('winSub').innerHTML=modNames[curModule]+'<br>双方都是 '+sc[0]+' 分';
    playTone(523,0.3,'sine',0.08);
  }}
  spawnConfetti();
  var best=parseInt(localStorage.getItem(sk)||'0');var mx=Math.max(sc[0],sc[1]);
  if(mx>best){{localStorage.setItem(sk,mx);}}
}}

function spawnConfetti(){{var colors=['#FF6B6B','#4ECDC4','#FFD700','#FF9800','#6C5CE7','#66BB6A','#EC407A','#42A5F5'];for(var i=0;i<60;i++){{var d=document.createElement('div');d.className='confetti';d.style.left=Math.random()*100+'%';d.style.top=-(Math.random()*50+10)+'px';d.style.width=(Math.random()*10+6)+'px';d.style.height=(Math.random()*10+6)+'px';d.style.background=colors[Math.floor(Math.random()*colors.length)];d.style.animationDuration=(Math.random()*2+2)+'s';d.style.animationDelay=Math.random()*1.5+'s';d.style.borderRadius=Math.random()>0.5?'50%':'0';document.body.appendChild(d);setTimeout(function(){{d.remove();}},4000);}}}}

function restartGame(){{clearInterval(ti);go=false;sc=[0,0];cr=0;ans=[false,false];
document.getElementById('s1').textContent='0';document.getElementById('s2').textContent='0';
document.getElementById('ansArea1').innerHTML='';document.getElementById('ansArea2').innerHTML='';
document.getElementById('fb1').innerHTML='';document.getElementById('fb2').innerHTML='';
document.getElementById('st1').textContent='';document.getElementById('st2').textContent='';
document.getElementById('rn').textContent='1';document.getElementById('tm').textContent='12';
document.getElementById('winOverlay').classList.remove('show');
document.getElementById('btnStart').style.display='inline-block';
document.getElementById('moduleBar').style.display='flex';
document.getElementById('q1').innerHTML='已选：'+modNames[curModule]+'<br>点击开始对战';
document.getElementById('q2').innerHTML='已选：'+modNames[curModule]+'<br>点击开始对战';
Q=sf(Q);var cf=document.querySelectorAll('.confetti');cf.forEach(function(c){{c.remove();}});}}

function backToMenu(){{restartGame();}}
</script>
</body>
</html>'''

def pkq(q, opts, ans):
    return {"q":q, "o1":opts, "a1":ans, "o2":opts, "a2":ans}

def dia(txt):
    """Put diagram text in a styled span"""
    return "<span class='diagram'>" + txt + "</span>"

# ============================================================
# 模块一：判断垂线和平行线
# ============================================================
m1 = [
    pkq("两条直线相交成直角时，这两条直线叫做什么？",
        ["互相平行", "互相垂直", "互相交叉", "互相重合"], 1),
    pkq("在同一平面内，永远不相交的两条直线叫做什么？",
        ["垂线", "斜线", "平行线", "曲线"], 2),
    pkq("长方形的长和宽是什么关系？",
        ["平行", "垂直", "重合", "既不平行也不垂直"], 1),
    pkq("长方形的两条长边是什么关系？",
        ["垂直", "平行", "交叉", "不确定"], 1),
    pkq(dia("A ───── B\nC ───── D") + "\n上图中直线AB和直线CD是什么关系？",
        ["垂直", "平行", "相交", "重合"], 1),
    pkq(dia("    │\n────┼────\n    │") + "\n上图中两条直线是什么关系？",
        ["平行", "垂直", "斜交", "重合"], 1),
    pkq("两条平行线之间的垂直线段长度有什么特点？",
        ["不相等", "处处相等", "越来越大", "越来越小"], 1),
    pkq("黑板的上边沿和下边沿是什么关系？",
        ["垂直", "平行", "相交", "不确定"], 1),
    pkq("正方形相邻的两条边是什么关系？",
        ["平行", "垂直", "重合", "不确定"], 1),
    pkq("同一平面内，过直线外一点可以画几条直线与已知直线平行？",
        ["0条", "1条", "2条", "无数条"], 1),
]

# ============================================================
# 模块二：画垂线
# ============================================================
m2 = [
    pkq("画垂线最常用的工具是什么？",
        ["直尺", "量角器", "三角板", "圆规"], 2),
    pkq("过直线上一点可以画几条垂线？",
        ["0条", "1条", "2条", "无数条"], 1),
    pkq("过直线外一点可以画几条垂线？",
        ["0条", "1条", "2条", "无数条"], 1),
    pkq("用三角板画垂线时，三角板的哪条边要紧贴已知直线？",
        ["斜边", "任意一条边", "一条直角边", "都可以"], 2),
    pkq("画垂线的第一步是什么？",
        ["直接画线", "用三角板直角边贴紧直线", "量出距离", "标出交点"], 1),
    pkq("验证两条直线是否垂直，最简单的方法是什么？",
        ["用直尺量", "用三角板的直角去比", "目测", "用圆规"], 1),
    pkq("两条直线互相垂直时，会形成几个直角？",
        ["1个", "2个", "3个", "4个"], 3),
    pkq("从直线外一点向这条直线画线段，哪种线段最短？",
        ["斜线段", "平行线段", "垂线段", "任意线段"], 2),
    pkq("用三角板画垂线，需要用到三角板的什么角？",
        ["锐角", "直角", "钝角", "任意角"], 1),
    pkq("两条直线垂直时，它们的交点叫做什么？",
        ["交点", "垂足", "顶点", "中点"], 1),
]

# ============================================================
# 模块三：点到直线的距离 + 测量
# ============================================================
m3 = [
    pkq("从直线外一点到这条直线的距离，是指什么？",
        ["任意线段的长", "垂直线段的长", "斜线段的长", "最长的线段"], 1),
    pkq("从直线外一点向直线画线段，可以画多少条？",
        ["1条", "2条", "10条", "无数条"], 3),
    pkq("点到直线的所有连线中，哪条最短？",
        ["垂线段", "斜线段", "水平线段", "都一样"], 0),
    pkq("测量点到直线的距离，实际是测量什么？",
        ["斜线长度", "垂线段的长度", "任意线段", "曲线长度"], 1),
    pkq("直尺上相邻两个刻度之间的距离是多少？",
        ["1毫米", "1厘米", "1分米", "根据尺子而定"], 0),
    pkq("测量时，直尺的哪端要对准起点？",
        ["0刻度", "1刻度", "任意刻度", "顶端"], 0),
    pkq("一条线段长5厘米，等于多少毫米？",
        ["5毫米", "50毫米", "500毫米", "0.5毫米"], 1),
    pkq("用直尺测量时，视线应该怎样看？",
        ["斜着看", "垂直看刻度", "从侧面看", "怎么看都行"], 1),
    pkq("点A到直线L的垂线段长3cm，那么点A到L的距离是多少？",
        ["1.5cm", "3cm", "6cm", "不能确定"], 1),
    pkq("要把直线外的点和直线上最近的点连起来，应该画什么线？",
        ["平行线", "垂线", "斜线", "曲线"], 1),
]

# ============================================================
# 模块四：画平行线之间的距离 + 测量
# ============================================================
m4 = [
    pkq("两条平行线之间的垂线段长度有什么特点？",
        ["左边大右边小", "右边大左边小", "处处相等", "中间最大"], 2),
    pkq("测量平行线之间的距离，应该怎样量？",
        ["斜着量", "垂直于两条平行线量", "平行于其中一条量", "怎么量都行"], 1),
    pkq("平行线之间可以画多少条垂线段？",
        ["1条", "2条", "10条", "无数条"], 3),
    pkq("两条平行线之间的距离是3cm，在其中间任意位置画垂线段，长度是多少？",
        ["1.5cm", "3cm", "6cm", "位置不同，长度不同"], 1),
    pkq("画平行线时，最常用的方法是什么？",
        ["用三角板和直尺配合", "只用三角板", "只用直尺", "徒手画"], 0),
    pkq("用直尺和三角板画平行线，三角板的作用是什么？",
        ["画直线", "贴紧直尺滑动", "测量距离", "固定直尺"], 1),
    pkq("两条平行线之间画的所有垂线段，它们互相之间是什么关系？",
        ["互相垂直", "互相平行", "互相交叉", "不一定"], 1),
    pkq(dia("A ───── B\n   3cm\nC ───── D") + "\n如果测得AB和CD之间任意位置的垂线段都长3cm，说明什么？",
        ["AB和CD相交", "AB和CD平行", "AB和CD垂直", "AB和CD不平行"], 1),
    pkq("在同一平面内，如果两条直线都与第三条直线平行，那么这两条直线之间是什么关系？",
        ["互相垂直", "互相平行", "相交", "不确定"], 1),
    pkq("测量平行线间距离时，如果测量结果不相等，说明什么？",
        ["尺子坏了", "两条线不平行", "测量方法不对", "距离本来就不等"], 1),
]

# ============================================================
# 模块五：长方形和正方形特征的认识
# ============================================================
m5 = [
    pkq("长方形有几条边？",
        ["3条", "4条", "5条", "6条"], 1),
    pkq("长方形有几条对称轴？",
        ["1条", "2条", "3条", "4条"], 1),
    pkq("长方形对边的长度有什么特点？",
        ["一条长一条短", "对边相等", "四条边都相等", "不一定"], 1),
    pkq("长方形有几个角？每个角是多少度？",
        ["4个锐角", "4个直角", "2个直角2个锐角", "4个钝角"], 1),
    pkq("正方形四条边的长度有什么特点？",
        ["对边相等", "四条边都相等", "相邻两边相等", "不一定"], 1),
    pkq("正方形有几条对称轴？",
        ["1条", "2条", "3条", "4条"], 3),
    pkq("正方形是特殊的长方形吗？",
        ["是的，正方形是特殊的长方形", "不是", "长方形是特殊的正方形", "两者无关"], 0),
    pkq("长方形和正方形的共同特点是什么？",
        ["四条边都相等", "四个角都是直角", "都是斜的", "没有共同点"], 1),
    pkq("一个四边形，四个角都是直角，四条边都相等，这是什么图形？",
        ["长方形", "正方形", "平行四边形", "梯形"], 1),
    pkq("一个四边形，四个角都是直角，对边相等但邻边不相等，这是什么图形？",
        ["正方形", "长方形", "平行四边形", "菱形"], 1),
]

# ============================================================
# 模块六：画长方形和正方形
# ============================================================
m6 = [
    pkq("画长方形时，至少需要知道哪两个条件？",
        ["边长和角度", "长和宽", "周长和面积", "对角线的长"], 1),
    pkq("画正方形时，至少需要知道什么？",
        ["长和宽", "对角线的长", "边长", "周长"], 2),
    pkq("画长方形时，先画什么？",
        ["直接画四条边", "先画一条长边（或宽）", "先画对角线", "先画四个角"], 1),
    pkq("画好长方形的一条边后，下一步做什么？",
        ["直接画对边", "在两端画垂线（宽）", "连接对角线", "量周长"], 1),
    pkq("画长方形时，需要用三角板画什么？",
        ["平行线", "直角（垂线）", "斜线", "曲线"], 1),
    pkq("一个长方形长6cm宽4cm，画图时应画几条线段？",
        ["2条", "4条", "6条", "8条"], 1),
    pkq("画正方形时，第一步画一条边，第二步画什么？",
        ["画对边", "在两端画与边长相等的垂线段", "连接对角线", "随便画"], 1),
    pkq("画长方形时，用什么工具确保四个角都是直角？",
        ["直尺", "三角板", "圆规", "量角器或三角板"], 3),
    pkq("画一个长5cm宽3cm的长方形，需要画几条线段？每条多长？",
        ["4条，都是5cm", "4条，两条5cm两条3cm", "4条，都是3cm", "2条"], 1),
    pkq("用直尺和三角板画长方形，三角板的作用是什么？",
        ["测量长度", "画垂线（确保直角）", "画平行线", "没什么用"], 1),
]

# ============================================================
# Verify & Generate
# ============================================================
all_modules = [m1, m2, m3, m4, m5, m6]
for i, m in enumerate(all_modules):
    assert len(m) == 10, f"Module {i+1}: expected 10, got {len(m)}"

def serialize(qlist):
    return [{"q":q.get("q",""),"q1":q.get("q1",""),"q2":q.get("q2",""),
             "o1":q["o1"],"a1":q["a1"],"o2":q["o2"],"a2":q["a2"]} for q in qlist]

all_json = json.dumps([serialize(m) for m in all_modules], ensure_ascii=False)
html = T.format(title="长方形和正方形", all_questions=all_json)

fp = os.path.join(BASE, "长方形和正方形-六合一PK.html")
with open(fp, 'w', encoding='utf-8') as f:
    f.write(html)
print("OK: %s" % fp)
print("Done!")
