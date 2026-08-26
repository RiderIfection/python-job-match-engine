"""Small, explainable job matcher using token weights and cosine similarity."""
import argparse, json, math, re
from collections import Counter
from pathlib import Path

STOP={"and","the","with","for","to","of","a","in","is","on","an"}
def tokens(text): return [w for w in re.findall(r"[a-z0-9+#.]+",text.lower()) if w not in STOP and len(w)>1]
def vector(text): return Counter(tokens(text))
def cosine(a,b):
    dot=sum(v*b.get(k,0) for k,v in a.items()); denom=math.sqrt(sum(v*v for v in a.values())*sum(v*v for v in b.values()))
    return dot/denom if denom else 0.0
def rank(profile,jobs):
    pv=vector(profile); results=[]
    for job in jobs:
        jv=vector(job["description"]); shared=sorted(set(pv)&set(jv),key=lambda k:jv[k]*pv[k],reverse=True)
        results.append({"id":job["id"],"title":job["title"],"score":round(cosine(pv,jv)*100,1),"matched_keywords":shared[:8]})
    return sorted(results,key=lambda x:x["score"],reverse=True)
def run(profile_path,jobs_path,output):
    result=rank(Path(profile_path).read_text(encoding="utf-8"),json.loads(Path(jobs_path).read_text(encoding="utf-8")))
    Path(output).write_text(json.dumps(result,indent=2),encoding="utf-8"); return result

def launch_gui():
    import tkinter as tk
    from tkinter import messagebox, scrolledtext
    here=Path(__file__).resolve().parent; root=tk.Tk(); root.title("Job Match Engine"); root.geometry("820x650")
    tk.Label(root,text="Explainable Job Match Engine",font=("Segoe UI",20,"bold")).pack(pady=12); tk.Label(root,text="Perfil / competencias").pack(anchor="w",padx=20)
    profile=scrolledtext.ScrolledText(root,height=7,font=("Segoe UI",10)); profile.pack(fill="x",padx=20); profile.insert("1.0",(here/"mockdata"/"profile_backend.txt").read_text(encoding="utf-8"))
    tk.Label(root,text="Resultados",font=("Segoe UI",11,"bold")).pack(anchor="w",padx=20,pady=(12,0)); output=scrolledtext.ScrolledText(root,font=("Consolas",10)); output.pack(fill="both",expand=True,padx=20,pady=6)
    def execute():
        try:
            jobs=json.loads((here/"mockdata"/"jobs_mock.json").read_text(encoding="utf-8")); result=rank(profile.get("1.0","end"),jobs); (here/"matches.json").write_text(json.dumps(result,indent=2),encoding="utf-8"); output.delete("1.0","end"); output.insert("end",json.dumps(result,indent=2)); messagebox.showinfo("Concluido",f"Melhor correspondencia: {result[0]['title']}")
        except Exception as exc: messagebox.showerror("Erro",str(exc))
    tk.Button(root,text="Calcular correspondencias",font=("Segoe UI",11,"bold"),bg="#1769aa",fg="white",command=execute).pack(pady=12); root.mainloop()
if __name__=="__main__":
    here=Path(__file__).resolve().parent
    p=argparse.ArgumentParser(); p.add_argument("profile",nargs="?"); p.add_argument("jobs",nargs="?"); p.add_argument("--output",default=str(here/"matches.json")); p.add_argument("--cli",action="store_true"); a=p.parse_args()
    if not a.cli and not a.profile and not a.jobs:
        from dashboard import launch
        launch()
    else: print(json.dumps(run(a.profile or str(here/"profile.txt"),a.jobs or str(here/"jobs.json"),a.output),indent=2))
