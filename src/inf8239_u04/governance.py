import hashlib
from pathlib import Path
import pandas as pd
import yaml
from . import __version__

def load_config(path="configs/governance.yml"):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def validate_raci(df):
    required={"activity","R","A","C","I"}
    if required-set(df.columns): raise ValueError("RACI columns missing")
    if df[["R","A"]].fillna("").apply(lambda s:s.str.strip().eq("")).any().any(): raise ValueError("Every activity needs R and A")
    if df["A"].astype(str).str.contains(r",|;|/| and ",regex=True).any(): raise ValueError("Every activity needs exactly one Accountable")
    return True

def deployment_decision(metrics, gaps, resources, gates):
    checks={
      "recall": metrics["recall"] >= gates["min_recall"],
      "recall_gap": gaps["recall_gap"] <= gates["max_recall_gap"],
      "fpr_gap": gaps["fpr_gap"] <= gates["max_fpr_gap"],
      "latency": resources["latency_ms"] <= gates["max_latency_ms"],
      "model_size": resources["model_kb"] <= gates["max_model_kb"],
    }
    # A global average can hide a localized failure: every group must reach the recall floor too.
    if "min_group_recall" in gates and "min_group_recall" in metrics: checks["group_recall"]=metrics["min_group_recall"] >= gates["min_group_recall"]
    failed=[k for k,v in checks.items() if not v]
    return {"status":"GO" if not failed else "REVIEW", "checks":checks, "failed":failed, "human_action":"Document review and final decision"}

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]

def traceable_record(result, cfg, kind="logistic", data_path="data/territorial_risk_synthetic.csv", config_path="configs/governance.yml"):
    decision=result["decision"]
    return {
      "status":decision["status"], "failed":decision["failed"], "checks":decision["checks"],
      "version":{"package":__version__,"model":kind,"data_sha256":sha256(data_path),"config_sha256":sha256(config_path)},
      "policy":{"system":cfg["system_name"],"policy_version":cfg["policy_version"],"gates":cfg["gates"],"prohibited_uses":cfg["prohibited_uses"],"safe_baseline":cfg["safe_baseline"]},
      "evidence":{"metrics":result["metrics"],"gaps":result["gaps"],"resources":result["resources"],"by_group":result["by_group"][["count","recall","fpr"]].round(3).to_dict(orient="index")},
      "human_action":"REVIEW: the Product Owner must analyse the evidence and record the final decision; the DSS only orders the review queue." if decision["status"]!="GO" else "GO: the Product Owner still confirms and records the decision before any use.",
    }
