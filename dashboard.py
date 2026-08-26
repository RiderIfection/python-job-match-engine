import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared_dashboard import shell, serve_dashboard
from matcher import rank

HERE=Path(__file__).resolve().parent; PROFILE=(HERE/"mockdata"/"profile_backend.txt").read_text(encoding="utf-8"); JOBS=HERE/"mockdata"/"jobs_mock.json"
BODY=r"""<div class='cards'><div class='card'><label>Vagas analisadas</label><div class='metric' id='count'>12</div><div class='hint'>Conjunto de demonstração</div></div><div class='card'><label>Melhor compatibilidade</label><div class='metric' id='best'>-</div><div class='hint'>Similaridade textual</div></div><div class='card'><label>Competências coincidentes</label><div class='metric' id='skills'>-</div><div class='hint'>Na melhor vaga</div></div><div class='card'><label>Vagas acima de 25%</label><div class='metric' id='strong'>-</div><div class='hint'>Correspondência relevante</div></div></div>
<div class='grid'><div class='panel'><h2>Ranking de oportunidades</h2><div class='sub'>Resultados explicáveis, ordenados por compatibilidade</div><div id='ranking' class='empty'>Calcula as correspondências para ver o ranking.</div></div><div class='panel'><h2>Perfil técnico</h2><div class='sub'>Edita as competências antes de calcular</div><textarea id='profile' class='field'>__PROFILE__</textarea><div class='notice' style='margin-top:15px'>A pontuação compara palavras e frequência. Não representa uma decisão de contratação.</div></div></div>
<script>const btn=document.getElementById('primaryAction');btn.textContent='Calcular ranking';btn.onclick=go;async function go(){document.body.classList.add('loading');let r=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({profile:profile.value})}),d=await r.json();document.body.classList.remove('loading');if(d.error)return alert(d.error);count.textContent=d.length;best.textContent=d[0].score+'%';skills.textContent=d[0].matched_keywords.length;strong.textContent=d.filter(x=>x.score>=25).length;ranking.innerHTML=d.map((x,i)=>`<div class='progress-row'><span><b>${i+1}. ${x.title}</b><small style='display:block;color:#65758b'>${x.matched_keywords.join(', ')||'Sem palavras coincidentes'}</small></span><div class='track'><div class='fill' style='width:${x.score}%'></div></div><b>${x.score}%</b></div>`).join('')}go()</script>""".replace("__PROFILE__",PROFILE)

def launch():
    def action(payload): return rank(payload.get("profile",PROFILE),json.loads(JOBS.read_text(encoding="utf-8")))
    serve_dashboard(shell("CareerMatch","Correspondência explicável entre perfil e vagas","CM",BODY,"Calcular ranking"),action,8014)
