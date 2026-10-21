from inf8239_u04.data import load_data
from inf8239_u04.dss import prioritized_queue,safe_baseline_flag
from inf8239_u04.governance import load_config
from inf8239_u04.pipeline import run
def _queue(status):
    r=run(load_data(),load_config()["gates"]); return prioritized_queue(r["model"],r["test"],status),r["test"]
def test_queue_is_explainable_and_hides_protected_group():
    q,test=_queue("REVIEW")
    assert len(q)==len(test) and q.probability.between(0,1).all() and list(q.priority)==list(range(1,len(q)+1))
    assert "protected_group" not in q.columns and q.explanation.str.len().gt(0).all()
def test_shadow_mode_queue_follows_safe_baseline():
    q,test=_queue("REVIEW"); first=int(safe_baseline_flag(test).sum())
    assert q.rule_first.iloc[:first].all() and q.recommended_action.str.contains("regla base").all()
def test_go_queue_follows_model_probability():
    q,_=_queue("GO"); assert q.probability.is_monotonic_decreasing
