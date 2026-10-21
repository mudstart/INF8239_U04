import json, time
from pathlib import Path
import numpy as np, pandas as pd
from inf8239_u04.data import load_data,features,temporal_split
from inf8239_u04.fairness import audit,intersectional,gap
from inf8239_u04.model import build_model
MIN_N=20; MIN_POS=10; B=1000
out=Path("reports/lab12"); out.mkdir(parents=True,exist_ok=True)
df=load_data(); train,test=temporal_split(df); y=test.target.reset_index(drop=True); g=test.protected_group.reset_index(drop=True)
# Non-predictive rule from LAB11: FIFO, moving up cases with >=3 previous incidents or exposure >0.7
preds={"rule_baseline":((test.previous_incidents>=3)|(test.exposure>0.7)).astype(int).to_numpy()}
for kind in ["logistic","tree"]:
    m=build_model(kind).fit(features(train),train.target); start=time.perf_counter(); preds[kind]=m.predict(features(test)); preds[kind+"_latency_ms"]=(time.perf_counter()-start)*1000/len(test)
def recall_gap(yy,pp,gg):
    r=[pp[(gg==k)&(yy==1)].mean() for k in ["G1","G2"]]; return abs(r[0]-r[1])
rng=np.random.default_rng(42); rows=[]
for name in ["rule_baseline","logistic","tree"]:
    p=pd.Series(preds[name]); overall,by_group,_=audit(y,p,g)
    boot=[]
    for _ in range(B):
        i=rng.integers(0,len(y),len(y)); boot.append(recall_gap(y.iloc[i].to_numpy(),p.iloc[i].to_numpy(),g.iloc[i].to_numpy()))
    lo,hi=np.percentile(boot,[2.5,97.5])
    rows.append({"model":name,"accuracy":overall["accuracy"],"recall":overall["recall"],"fpr":overall["fpr"],"selection_rate":overall["selection_rate"],
                 "recall_gap":gap(by_group,"recall"),"recall_gap_ci95":f"[{lo:.3f}, {hi:.3f}]","fpr_gap":gap(by_group,"fpr"),
                 "latency_ms":preds.get(name+"_latency_ms",0.0)})
    if name=="rule_baseline": by_group.to_csv(out/"rule_baseline_by_group.csv")
pd.DataFrame(rows).round(4).to_csv(out/"model_comparison.csv",index=False)
key=intersectional(test).reset_index(drop=True); support=pd.DataFrame({"count":key.value_counts(),"positives":key[y==1].value_counts()}).fillna(0).astype(int).sort_index()
support["interpretable"]=(support["count"]>=MIN_N)&(support["positives"]>=MIN_POS)
support.to_csv(out/"intersectional_support.csv")
(out/"support_policy.json").write_text(json.dumps({"min_group_n":MIN_N,"min_positives_for_recall":MIN_POS,"bootstrap_resamples":B,"seed":42},indent=2),encoding="utf-8")
print(pd.DataFrame(rows).round(3).to_string(index=False)); print(support)
