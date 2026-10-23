# diag22b launcher (Aethon, 2026-10-23) - IT1b power-law re-run [hive proposal, untested]. WRITTEN, NOT EXECUTED.
# Spec: out\diag22b\IT1B_POWERLAW_FROZEN.md (sha256 AE31015E...). Grading: it1b_measure.py via run.py it1b-grade.
# Rows: B10, alpha {1.0,0.5}, delta {0 (control, seed -1), 0.0015, 0.003} x seeds {0,1}, flow from t=0 to T cap 0.6, fit window t in [0.1,0.6].
# SHORT CHECK LIMIT [flagged for Venus]: stored diag22 rows only hold X(t) for t>=0.6, so the "match diag22 X_0 within 2%"
#   check can only compare ONE point: t=0.6, X=2.9027 (alpha=1, delta=0, out\diag22\it1\B10_a1.0_delta0.json).
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
function Row($name, [string[]]$a){
  $f = FreeGB
  if ($f -lt $MinFreeGB) { $script:fails += $name; Note 'CRASH' "diag22b row $name skipped: free RAM $f GB < $MinFreeGB GB (NOT COMPUTED)"; return }
  $t = Get-Date; & $Py -B run.py @a *> "$LG\$name.log"; $rc = $LASTEXITCODE
  Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b row {1} rc={2} {3:N0}s" -f (Get-Date), $name, $rc, ((Get-Date)-$t).TotalSeconds)
  if($rc -ne 0){ $script:fails += $name; Note 'CRASH' "diag22b row $name failed rc=$rc (log logs\diag22b\$name.log); continuing" }
}
Note 'LAUNCHED' "diag22b started PID $($PID): IT1b B10, cal + 2 controls + 8 delta rows, T cap 0.6"
Row 'cal' @('it1b-cal')
foreach($al in '1.0','0.5'){ Row "it1b_a${al}_delta0" @('it1b-row','--alpha',$al,'--seed','-1','--delta','0') }
foreach($dl in '0.0015','0.003'){ foreach($s in 0,1){ foreach($al in '1.0','0.5'){ Row "it1b_a${al}_s${s}_delta$dl" @('it1b-row','--alpha',$al,'--seed',"$s",'--delta',$dl) } } }
Row 'grade' @('it1b-grade')
$st = try { (Get-Content $G -Raw | ConvertFrom-Json).status } catch { 'no grade' }
try { & $Notify -Status 'DONE' -Summary "diag22b IT1b finished: $st; failed rows: $(if($fails){$fails -join ','}else{'none'}); tip probe held" -GradeFile $G -StatusFile $ST } catch {}
Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b DONE status={1} fails={2}" -f (Get-Date), $st, ($fails -join ','))
