"""J2 row wrapper (JAMMING_TEST_V3_FREEZE 5260f6c7). Script 42724a62 unchanged; sets only npz path, row and output. Usage: run_j2_row.py B OUT
uk_now is overridden with a safe version (logging only, no maths change): UK time, or a labelled UTC stamp if tz data is missing."""
import sys, os, importlib.util, datetime as dt
here = os.path.dirname(os.path.abspath(__file__)); lift = os.path.dirname(here)
p = os.path.join(lift, 'fuzz', 'cone', 'tools', 'hessian_b_softmode.py')
s = importlib.util.spec_from_file_location('h', p); h = importlib.util.module_from_spec(s); s.loader.exec_module(h)
def uk_now():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo('Europe/London')).strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception:
        return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC (tz fallback)')
h.uk_now = uk_now
b = float(sys.argv[1]); out = sys.argv[2]
h.NPZ = os.path.join(h.CONE, 'v2_1', 'sol_probeB_r3_S1_b{b:g}_n3_N81_seed0.npz'); h.ROWS = [b]
_row = h.row
def row(bb):
    r = _row(bb); print(f"b={bb} E_saved={r['E_saved']} E_model={r['E_model']} grad_norm_y={r['grad_norm_y']} dim_y={r['dim_y']}", flush=True); return r
h.row = row
sys.argv = ['hessian_b_softmode.py', '--out', out]; h.main()
