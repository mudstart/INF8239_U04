import pandas as pd
from inf8239_u04.data import load_data,temporal_split
from inf8239_u04.governance import load_config
from inf8239_u04.monitoring import drift_report,psi
def test_identical_samples_have_no_drift():
    s=load_data().exposure; assert psi(s,s)<1e-6
def test_shifted_sample_raises_alert():
    tr,te=temporal_split(load_data()); shifted=te.assign(exposure=(te.exposure+0.4).clip(upper=1))
    r=drift_report(tr,shifted,load_config()["monitoring"]).set_index("variable"); assert r.loc["exposure","status"]=="ALERT"
def test_current_window_has_no_drift_alert():
    tr,te=temporal_split(load_data()); assert (drift_report(tr,te,load_config()["monitoring"]).status!="ALERT").all()
