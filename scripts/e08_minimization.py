from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from inf8239_u04.data import load_data,temporal_split
from inf8239_u04.fairness import audit,gap
# Data minimization: does each categorical feature earn its place? Same logistic setup as build_model, dropping features one at a time.
NUM=["previous_incidents","infrastructure_score","exposure"]
VARIANTS={"current (zone + age_band)":["zone","age_band"],"without age_band":["zone"],"without zone and age_band":[]}
out=Path("reports/e08"); out.mkdir(parents=True,exist_ok=True)
train,test=temporal_split(load_data()); rows=[]
for name,cat in VARIANTS.items():
    prep=ColumnTransformer(([("cat",OneHotEncoder(handle_unknown="ignore"),cat)] if cat else [])+[("num",StandardScaler(),NUM)])
    model=make_pipeline(prep,LogisticRegression(max_iter=1200,class_weight="balanced",random_state=42)).fit(train[cat+NUM],train.target)
    overall,groups,_=audit(test.target,model.predict(test[cat+NUM]),test.protected_group)
    rows.append({"variant":name,"features":len(cat+NUM),"recall":overall["recall"],"fpr":overall["fpr"],"recall_G1":groups.loc["G1","recall"],"recall_G2":groups.loc["G2","recall"],
                 "recall_gap":gap(groups,"recall"),"fpr_gap":gap(groups,"fpr")})
result=pd.DataFrame(rows).round(3); result.to_csv(out/"minimization.csv",index=False); print(result.to_string(index=False))
