import json
from datetime import datetime,timezone
from pathlib import Path
import pandas as pd
from inf8239_u04.data import load_data,temporal_split
from inf8239_u04.governance import load_config,traceable_record
from inf8239_u04.monitoring import drift_report
from inf8239_u04.pipeline import run
# Monthly monitoring: data drift (PSI, training window vs. current window) plus the governed quality gates.
cfg=load_config(); df=load_data(); reference,current=temporal_split(df)
drift=drift_report(reference,current,cfg["monitoring"]); record=traceable_record(run(df,cfg["gates"]),cfg)
raci=pd.read_csv("student_inputs/raci.csv").set_index("activity")
alerts=[f"drift:{r.variable}" for r in drift.itertuples() if r.status=="ALERT"]+[f"gate:{g}" for g in record["failed"]]
report={"generated_at":datetime.now(timezone.utc).isoformat(),"policy_version":cfg["policy_version"],"version":record["version"],
        "reference_window":f"{reference.received_date.min().date()} to {reference.received_date.max().date()}","current_window":f"{current.received_date.min().date()} to {current.received_date.max().date()}",
        "drift":drift.to_dict(orient="records"),"gates":record["checks"],"status":record["status"],"alerts":alerts,
        "escalate_to":raci.loc["Monitoring and drift","A"] if alerts else None,"next_action":"Open the runbook (docs/RUNBOOK.md) and record the response" if alerts else "No action; next monthly run"}
out=Path("reports/monitoring"); out.mkdir(parents=True,exist_ok=True)
(out/"monitoring_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8"); drift.to_csv(out/"drift_psi.csv",index=False)
print(drift.to_string(index=False)); print("alerts:",alerts or "none")
