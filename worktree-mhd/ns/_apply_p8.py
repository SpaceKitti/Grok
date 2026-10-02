from pathlib import Path

NS = Path(r"C:\Users\Akitt\Grok\worktree-mhd\ns")
CH = NS / "chive_ns"

# --- compressible.py ---
p = CH / "compressible.py"
text = p.read_text(encoding="utf-8")
old_header = "# @Akitti C*Hive – Compressible MHD (patches 5+6, 7 Venus I_leak)"
new_header = "# @Akitti C*Hive – Compressible MHD (patches 5+6, 7 Venus I_leak, 8 Brio-Wu)"
if old_header not in text:
    raise SystemExit("header not found")
text = text.replace(old_header, new_header, 1)

old_fn = '''def brio_wu_fields(grid, gamma=GAMMA_DEFAULT):
    """Brio & Wu 1988 1D MHD Riemann on a 1D-like periodic 2D/3D grid.

    Left  (x < L/2):  rho=1,     p=1,   u=0, By=+1
    Right (x >= L/2): rho=0.125, p=0.1, u=0, By=-1
    Bx=0.75. gamma=5/3 in this tree. Sharp jump: spectral Gibbs ringing
    at the shocks is expected (no WENO/TVD/limiter).
    """
    del gamma
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, _Y = jnp.meshgrid(x, x, indexing="ij")
        z = jnp.zeros_like(X)
        left = X < (0.5 * L)
        rho = jnp.where(left, 1.0, 0.125)
        p = jnp.where(left, 1.0, 0.1)
        u = jnp.stack([z, z])
        Bx = jnp.full_like(X, 0.75)
        By = jnp.where(left, 1.0, -1.0)
        B = jnp.stack([Bx, By])
    else:
        X, _Y, _Z = jnp.meshgrid(x, x, x, indexing="ij")
        z = jnp.zeros_like(X)
        left = X < (0.5 * L)
        rho = jnp.where(left, 1.0, 0.125)
        p = jnp.where(left, 1.0, 0.1)
        u = jnp.stack([z, z, z])
        Bx = jnp.full_like(X, 0.75)
        By = jnp.where(left, 1.0, -1.0)
        B = jnp.stack([Bx, By, z])
    return u, rho, p, B
'''

new_fn = '''def brio_wu_fields(grid, gamma=2.0):
    """Brio & Wu 1988 1D MHD Riemann on a 1D-like periodic torus.

    Paper gamma is 2. Primitive left/right states do not depend on gamma;
    the arg is for the caller EOS/CFL. Hive GAMMA_DEFAULT stays 5/3;
    evolution gamma is test-local via mhd_params/ic_params.

    Left  (x < L/2):  rho=1,     p=1,   u=0, Bx=0.75, By=+1
    Right (x >= L/2): rho=0.125, p=0.1, u=0, Bx=0.75, By=-1

    Periodic wrap puts a second jump at x=0. Stop before waves meet
    (t < (L/4) / max(|u|+c_s+|v_A|)). Spectral Gibbs ringing is the
    scheme (rho may go negative); no floor, no WENO/TVD.
    """
    gamma = float(gamma)
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, _Y = jnp.meshgrid(x, x, indexing="ij")
        z = jnp.zeros_like(X)
        left = X < (0.5 * L)
        rho = jnp.where(left, 1.0, 0.125)
        p = jnp.where(left, 1.0, 0.1)
        u = jnp.stack([z, z])
        Bx = jnp.full_like(X, 0.75)
        By = jnp.where(left, 1.0, -1.0)
        B = jnp.stack([Bx, By])
    else:
        X, _Y, _Z = jnp.meshgrid(x, x, x, indexing="ij")
        z = jnp.zeros_like(X)
        left = X < (0.5 * L)
        rho = jnp.where(left, 1.0, 0.125)
        p = jnp.where(left, 1.0, 0.1)
        u = jnp.stack([z, z, z])
        Bx = jnp.full_like(X, 0.75)
        By = jnp.where(left, 1.0, -1.0)
        B = jnp.stack([Bx, By, z])
    return u, rho, p, B


def brio_wu_wrap_time(grid, gamma=2.0):
    """Earliest t at which the two periodic Riemann fans can meet.

    Jumps at x=0 and x=L/2; each fan travels at most L/4. Bound by
    max(|u| + c_s + |v_A|) on the IC. No floor.
    """
    gamma = float(gamma)
    u, rho, p, B = brio_wu_fields(grid, gamma=gamma)
    speed = jnp.sqrt(jnp.sum(u ** 2, axis=0))
    cs = jnp.sqrt(gamma * p / rho)
    vA = jnp.sqrt(jnp.sum(B ** 2, axis=0) / rho)
    vfast = jnp.max(speed + cs + vA)
    return 0.25 * float(grid["L"]) / (float(vfast) + 1e-30)
'''

if old_fn not in text:
    raise SystemExit("brio_wu_fields block not found")
text = text.replace(old_fn, new_fn, 1)
p.write_text(text, encoding="utf-8")
print("updated", p)

# --- __init__.py ---
p = CH / "__init__.py"
text = p.read_text(encoding="utf-8")
old = "    sound_wave_fields, brio_wu_fields, cfl_dt_cmhd, primitive_u_rhs, primitive_cmhd_step,"
new = "    sound_wave_fields, brio_wu_fields, brio_wu_wrap_time, cfl_dt_cmhd, primitive_u_rhs, primitive_cmhd_step,"
if old not in text:
    raise SystemExit("__init__ import line not found")
text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8")
print("updated", p)

# --- driver.py ---
p = CH / "driver.py"
text = p.read_text(encoding="utf-8")
old = "    sound_wave_fields, brio_wu_fields, cfl_dt_cmhd,"
new = "    sound_wave_fields, brio_wu_fields, cfl_dt_cmhd,"
# keep import; gamma fallbacks below
old = '''    if ic == "brio_wu":
        gamma = float((mhd_params or {}).get("gamma", GAMMA_DEFAULT))
        u, _rho, _p, _B = brio_wu_fields(grid, gamma=gamma)
        return u'''
new = '''    if ic == "brio_wu":
        gamma = float((mhd_params or {}).get(
            "gamma", p.get("gamma", 2.0)))
        u, _rho, _p, _B = brio_wu_fields(grid, gamma=gamma)
        return u'''
if old not in text:
    raise SystemExit("driver _initial_velocity brio_wu not found")
text = text.replace(old, new, 1)

old = "    brio_wu = Brio-Wu 1988 1D MHD Riemann (cmhd; spectral ringing expected)."
new = "    brio_wu = Brio-Wu 1988 1D MHD Riemann on the torus (cmhd; paper gamma=2 test-local; stop before wrap; spectral ringing expected)."
if old not in text:
    raise SystemExit("driver docstring brio_wu not found")
text = text.replace(old, new, 1)

old = '''            gamma_cfl = float(mhd_params.get("gamma", GAMMA_DEFAULT))'''
new = '''            gamma_cfl = float(mhd_params.get(
                "gamma", (ic_params or {}).get("gamma", GAMMA_DEFAULT)))'''
if old not in text:
    raise SystemExit("driver gamma_cfl not found")
text = text.replace(old, new, 1)

old = '''        gamma = float(mhd_params.get("gamma", GAMMA_DEFAULT))
        p0 = float(mhd_params.get("p0", 1.0))'''
new = '''        gamma = float(mhd_params.get(
            "gamma", (ic_params or {}).get("gamma", GAMMA_DEFAULT)))
        p0 = float(mhd_params.get("p0", 1.0))'''
if old not in text:
    raise SystemExit("driver cmhd gamma not found")
text = text.replace(old, new, 1)

p.write_text(text, encoding="utf-8")
print("updated", p)

# --- README ---
p = Path(r"C:\Users\Akitt\Grok\worktree-mhd\README.md")
text = p.read_text(encoding="utf-8")
old = '- **Brio-Wu:** ic="brio_wu" on mode="cmhd" (1D MHD Riemann). Spectral; ringing expected.'
new = '- **Brio–Wu:** `ic="brio_wu"` on mode="cmhd" is a 1D MHD Riemann problem on the periodic torus (stop before wrap). Spectral; Gibbs ringing expected (rho may go negative — that is the scheme, not a continuity leak). gamma=2 is test-local via mhd_params/ic_params; Hive GAMMA_DEFAULT stays 5/3. No WENO/TVD, no rho pin/floor. Success is waves exist, no NaN — not a plot match. Do not interpret smear vs ribbon. Alfvén on mode="mhd" is unchanged.'
if old not in text:
    raise SystemExit("README brio-wu bullet not found")
text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8")
print("updated", p)

print("OK")
