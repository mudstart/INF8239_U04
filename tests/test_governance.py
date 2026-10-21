import pandas as pd, pytest
from inf8239_u04.governance import deployment_decision,validate_raci
def test_failed_gate_requires_review():
    d=deployment_decision({"recall":.5},{"recall_gap":.1,"fpr_gap":.1},{"latency_ms":1,"model_kb":5},{"min_recall":.7,"max_recall_gap":.2,"max_fpr_gap":.2,"max_latency_ms":10,"max_model_kb":20}); assert d["status"]=="REVIEW"
def test_raci_requires_accountable():
    with pytest.raises(ValueError): validate_raci(pd.DataFrame([{"activity":"deploy","R":"ML","A":"","C":"DS","I":"Users"}]))
def test_raci_rejects_shared_accountable():
    with pytest.raises(ValueError,match="exactly one"): validate_raci(pd.DataFrame([{"activity":"deploy","R":"ML","A":"PO and DS","C":"DS","I":"Users"}]))
def test_project_raci_is_valid():
    assert validate_raci(pd.read_csv("student_inputs/raci.csv"))
def test_group_recall_gate_requires_review():
    gates={"min_recall":.6,"min_group_recall":.7,"max_recall_gap":.2,"max_fpr_gap":.2,"max_latency_ms":10,"max_model_kb":20}
    d=deployment_decision({"recall":.72,"min_group_recall":.65},{"recall_gap":.1,"fpr_gap":.1},{"latency_ms":1,"model_kb":5},gates); assert d["status"]=="REVIEW" and d["failed"]==["group_recall"]
def test_recommendation_is_traceable():
    from inf8239_u04.data import load_data
    from inf8239_u04.governance import load_config,traceable_record
    from inf8239_u04.pipeline import run
    cfg=load_config(); r=traceable_record(run(load_data(),cfg["gates"]),cfg)
    assert {"version","policy","evidence","human_action"}<=set(r) and r["version"]["data_sha256"] and r["policy"]["policy_version"]
