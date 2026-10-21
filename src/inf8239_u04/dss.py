import numpy as np
import pandas as pd
from .data import features

BANDS=[(0.7,"Alta"),(0.5,"Media"),(0.0,"Baja")]

def safe_baseline_flag(df):
    return (df.previous_incidents>=3)|(df.exposure>0.7)

def explain(model, X, top=2):
    # Linear contribution of each transformed feature (coefficient x value); only meaningful for the logistic model.
    prep,clf=model.steps[0][1],model.steps[-1][1]
    if not hasattr(clf,"coef_"): return pd.Series([""]*len(X),index=X.index)
    Z=prep.transform(X); Z=Z.toarray() if hasattr(Z,"toarray") else Z
    label=lambda n:next((f"{c}={n[len(c)+1:]}" for c in ["zone","age_band"] if n.startswith(c+"_")),n)
    names=[label(n.split("__",1)[1]) for n in prep.get_feature_names_out()]
    contrib=Z*clf.coef_[0]
    return pd.Series([", ".join(f"{names[j]} ({'+' if c[j]>0 else '-'})" for j in np.argsort(-np.abs(c))[:top]) for c in contrib],index=X.index)

def prioritized_queue(model, cases, status):
    X=features(cases); proba=model.predict_proba(X)[:,1]; rule=safe_baseline_flag(cases)
    q=pd.DataFrame({"case_id":cases.case_id,"received_date":cases.received_date.dt.date,"zone":cases.zone,
                    "probability":proba.round(3),"model_band":[next(b for t,b in BANDS if p>=t) for p in proba],
                    "rule_first":rule,"explanation":explain(model,X)})
    if status=="GO":
        q["recommended_action"]=q.model_band.map({"Alta":"Revisar primero","Media":"Revisión estándar","Baja":"Orden de llegada"})
        q=q.sort_values("probability",ascending=False)
    else:
        # Shadow mode: the safe baseline orders the queue; the model is shown only as advisory evidence.
        q["recommended_action"]=np.where(q.rule_first,"Revisar primero (regla base)","Orden de llegada (regla base)")
        q=q.sort_values(["rule_first","received_date"],ascending=[False,True])
    q["discrepancy"]=(q.model_band=="Alta")&~q.rule_first | (q.model_band=="Baja")&q.rule_first
    q.insert(0,"priority",range(1,len(q)+1))
    return q.reset_index(drop=True)
