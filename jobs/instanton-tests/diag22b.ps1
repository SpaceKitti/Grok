# diag22b launcher (Aethon, 2026-10-23) - IT1b fix round 1, fixed-time chi at t=0.6 [hive proposal, untested]. WRITTEN, NOT EXECUTED.
# Spec: out\diag22b\IT1B_FIXEDTIME_FROZEN.md (sha256 C99963A0, replaces FD9FD866). Grading: it1b_measure.py via run.py it1b-grade.
# Label: linear response at t=0.6, reduced model. STEP 0: BPST pre-step (run.py it1b-bpst, B10, h=1,2/3,1/2); FAIL => stop, no rows.
# Existing alpha=1 delta=0 row (rows\B10_a1.0_s-1_delta0.0.json) is reused by the resume skip.
# Rows: B10, alpha {1.0,0.5}, delta {0 (control, seed -1), 0.0015, 0.003} x seeds {0,1}, flow from t=0 to T cap 0.6, fit window t in [0.1,0.6].
# SHORT CHECK LIMIT [flagged for Venus]: stored diag22 rows only hold X(t) for t>=0.6, so the "match diag22 X_0 within 2%"
#   check can only compare ONE point: t=0.6, X=2.9027 (alpha=1, delta=0, out\diag22\it1\B10_a1.0_delta0.json).
# REDUCED MODEL run. Resume: rows/cal already on disk are skipped (checkpoint per alpha,delta,seed).
# Tip probe NOT included (held until IT1b graded).
param([double]$MinFreeGB = 3.3)
$ErrorActionPreference = 'Continue'
$D = 'C:\Users\Akitt\Grok\jobs\instanton-tests'; Set-Location $D
$Py = 'C:\Users\Akitt\Grok\.venv\Scripts\python.exe'; $Notify = 'C:\Users\Akitt\Grok\jobs\notify.ps1'
$ST = "$D\out\STATUS.txt"; $G = "$D\out\diag22b\it1b_grade.json"; $LG = "$D\logs\diag22b"
New-Item -ItemType Directory -Force $LG, "$D\out\diag22b\rows" | Out-Null
$env:PYTHONIOENCODING = 'utf-8'; $fails = @()
function Note($s, $m){ Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b {1}: {2}" -f (Get-Date), $s, $m); try { & $Notify -Status $s -Summary $m -StatusFile $ST } catch { Add-Content $ST "NOTIFY ERROR: $($_.Exception.Message)" } }
function FreeGB { [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB, 2) }
$f = FreeGB
if ($f -lt $MinFreeGB) { Note 'CRASH' "diag22b refused: free RAM $f GB < guard $MinFreeGB GB; nothing run"; exit 2 }
function Resolve-Out([string[]]$a){
  $ci = [Globalization.CultureInfo]::InvariantCulture
  if ($a[0] -eq 'it1b-cal') { return "$D\out\diag22b\cal_B10.json" }
  if ($a[0] -eq 'it1b-row') { $al = [double]::Parse($a[2], $ci); $s = [int]$a[4]; $dl = [double]::Parse($a[6], $ci)
    return ("$D\out\diag22b\rows\B10_a{0}_s{1}_delta{2}.json" -f $al.ToString('0.0###', $ci), $s, $dl.ToString('0.0###', $ci)) }
  return $null }
function Row($name, [string[]]$a){
  $out = Resolve-Out $a
  if ($out -and (Test-Path $out)) { Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b row {1} SKIP (resume: exists)" -f (Get-Date), $name); return }
  $f = FreeGB
  if ($f -lt $MinFreeGB) { $script:fails += $name; Note 'CRASH' "diag22b row $name skipped: free RAM $f GB < $MinFreeGB GB (NOT COMPUTED)"; return }
  $t = Get-Date; & $Py -B run.py @a *> "$LG\$name.log"; $rc = $LASTEXITCODE
  Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b row {1} rc={2} {3:N0}s" -f (Get-Date), $name, $rc, ((Get-Date)-$t).TotalSeconds)
  if($rc -ne 0){ $script:fails += $name; Note 'CRASH' "diag22b row $name failed rc=$rc (log logs\diag22b\$name.log); continuing" }
}
Note 'LAUNCHED' "diag22b started PID $($PID): IT1b B10, cal + 2 controls + 8 delta rows, T cap 0.6, BPST pre-step first"
$BP = "$D\out\diag22b\bpst_prestep.json"
$bpOk = $false; if (Test-Path $BP) { try { $bpOk = [bool](Get-Content $BP -Raw | ConvertFrom-Json).ok } catch { $bpOk = $false } }
if ($bpOk) { Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b row bpst SKIP (resume: passed on disk)" -f (Get-Date)) }
else {
  $f = FreeGB
  if ($f -lt $MinFreeGB) { Note 'CRASH' "diag22b BPST pre-step refused: free RAM $f GB < $MinFreeGB GB; no rows run"; exit 2 }
  $t = Get-Date; & $Py -B run.py it1b-bpst --box B10 *> "$LG\bpst.log"; $rc = $LASTEXITCODE
  Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b row bpst rc={1} {2:N0}s" -f (Get-Date), $rc, ((Get-Date)-$t).TotalSeconds)
  if ($rc -ne 0) {
    $why = if ($rc -eq 3) { 'BPST pre-step FAILED (S/8pi^2 not within 1% of target after h->0 fit)' } else { "BPST pre-step error rc=$rc" }
    try { & $Notify -Status 'FAIL' -Summary "diag22b stopped: $why; no IT1b rows run (log logs\diag22b\bpst.log)" -GradeFile $BP -StatusFile $ST } catch {}
    Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b DONE status=BPST-PRESTEP-STOP rc={1}" -f (Get-Date), $rc); exit 3 }
}
Row 'cal' @('it1b-cal')
foreach($al in '1.0','0.5'){ Row "it1b_a${al}_delta0" @('it1b-row','--alpha',$al,'--seed','-1','--delta','0') }
foreach($dl in '0.0015','0.003'){ foreach($s in 0,1){ foreach($al in '1.0','0.5'){ Row "it1b_a${al}_s${s}_delta$dl" @('it1b-row','--alpha',$al,'--seed',"$s",'--delta',$dl) } } }
Row 'grade' @('it1b-grade')
$st = try { (Get-Content $G -Raw | ConvertFrom-Json).status } catch { 'no grade' }
try { & $Notify -Status 'DONE' -Summary "diag22b IT1b finished: $st; failed rows: $(if($fails){$fails -join ','}else{'none'}); tip probe held" -GradeFile $G -StatusFile $ST } catch {}
Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b DONE status={1} fails={2}" -f (Get-Date), $st, ($fails -join ','))
