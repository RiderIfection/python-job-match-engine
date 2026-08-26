import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared_dashboard import shell, serve_dashboard
from matcher import rank

HERE=Path(__file__).resolve().parent; PROFILE=(HERE/"mockdata"/"profile_backend.txt").read_text(encoding="utf-8"); JOBS=HERE/"mockdata"/"jobs_mock.json"
BODY=r"""<div class='cards'><div class='card'><label>Jobs analysed</label><div class='metric' id='count'>12</div><div class='hint'>Demo dataset</div></div><div class='card'><label>Best match</label><div class='metric' id='best'>-</div><div class='hint'>Text similarity</div></div><div class='card'><label>Matching skills</label><div class='metric' id='skills'>-</div><div class='hint'>In the best-matching job</div></div><div class='card'><label>Jobs above 25%</label><div class='metric' id='strong'>-</div><div class='hint'>Relevant match</div></div></div>
<div class='grid'><div class='panel'><h2>Opportunity ranking</h2><div class='sub'>Explainable results ranked by compatibility</div><div id='ranking' class='empty'>Calculate matches to view the ranking.</div></div><div class='panel'><h2>Technical profile</h2><div class='sub'>Edit the skills before calculating</div><textarea id='profile' class='field'>__PROFILE__</textarea><div class='notice' style='margin-top:15px'>The score compares words and frequency. It does not represent a hiring decision.</div></div></div>
<script>const btn=document.getElementById('primaryAction');btn.textContent='Calculate ranking';btn.onclick=go;async function go(){document.body.classList.add('loading');let r=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({profile:profile.value})}),d=await r.json();document.body.classList.remove('loading');if(d.error)return alert(d.error);count.textContent=d.length;best.textContent=d[0].score+'%';skills.textContent=d[0].matched_keywords.length;strong.textContent=d.filter(x=>x.score>=25).length;ranking.innerHTML=d.map((x,i)=>`<div class='progress-row'><span><b>${i+1}. ${x.title}</b><small style='display:block;color:#65758b'>${x.matched_keywords.join(', ')||'No matching keywords'}</small></span><div class='track'><div class='fill' style='width:${x.score}%'></div></div><b>${x.score}%</b></div>`).join('')}go()</script>""".replace("__PROFILE__",PROFILE)

def launch():
    def action(payload): return rank(payload.get("profile",PROFILE),json.loads(JOBS.read_text(encoding="utf-8")))
    serve_dashboard(shell("CareerMatch","Explainable matching between profiles and jobs","CM",BODY,"Calculate ranking"),action,8014)
