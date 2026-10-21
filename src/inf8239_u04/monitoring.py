import numpy as np
import pandas as pd

NUMERIC=["previous_incidents","infrastructure_score","exposure"]
CATEGORICAL=["zone","age_band","protected_group"]

def psi(reference, current, bins=10, eps=1e-4):
    """Population Stability Index between a reference and a current sample."""
    if pd.api.types.is_numeric_dtype(reference):
        edges=np.unique(np.quantile(reference,np.linspace(0,1,bins+1))); edges[0],edges[-1]=-np.inf,np.inf
        ref=pd.cut(reference,edges).value_counts(normalize=True,sort=False); cur=pd.cut(current,edges).value_counts(normalize=True,sort=False)
    else:
        cats=sorted(set(reference)|set(current)); ref=reference.value_counts(normalize=True).reindex(cats,fill_value=0); cur=current.value_counts(normalize=True).reindex(cats,fill_value=0)
    ref,cur=ref.to_numpy()+eps,cur.to_numpy()+eps
    return float(np.sum((cur-ref)*np.log(cur/ref)))

def drift_report(reference, current, thresholds):
    rows=[]
    for col in NUMERIC+CATEGORICAL+["target"]:
        value=psi(reference[col],current[col])
        status="ALERT" if value>=thresholds["psi_alert"] else "WARN" if value>=thresholds["psi_warn"] else "OK"
        rows.append({"variable":col,"psi":round(value,4),"status":status})
    return pd.DataFrame(rows)
