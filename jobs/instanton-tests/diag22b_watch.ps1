# diag22b crash watcher (Aethon, 2026-10-23). Local only, NO bot calls. Checks the runner PID every $Every min.
# If the runner dies without a "diag22b DONE" line: notify.ps1 -Status CRASH, then resume ONCE (MaxResume) by relaunching
# diag22b.ps1, which skips rows already on disk (checkpoint per alpha,delta,seed). REDUCED MODEL run.
param([Parameter(Mandatory)][int]$RunnerPid, [int]$Every = 20, [int]$MaxResume = 1)
$D = 'C:\Users\Akitt\Grok\jobs\instanton-tests'; $ST = "$D\out\STATUS.txt"; $Notify = 'C:\Users\Akitt\Grok\jobs\notify.ps1'
$start = Get-Date; $resumes = 0
function Log($m){ Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} diag22b-watch: {1}" -f (Get-Date), $m) }
Log "watching PID $RunnerPid every $Every min (watcher PID $PID, max resumes $MaxResume)"
while ($true) {
  Start-Sleep -Seconds ($Every*60)
  if (Get-Process -Id $RunnerPid -ErrorAction SilentlyContinue) { continue }
  $done = Select-String $ST -Pattern 'diag22b DONE' -SimpleMatch -ErrorAction SilentlyContinue | ? { try { [datetime]($_.Line.Substring(0,19)) -ge $start } catch { $false } }
  if ($done) { Log "runner exited after DONE; watcher exits"; exit 0 }
  $m = "diag22b runner PID $RunnerPid died without DONE (watcher)"
  if ($resumes -lt $MaxResume) { $m += "; resuming (skip finished rows)" }
  Log "CRASH $m"; try { & $Notify -Status 'CRASH' -Summary $m -StatusFile $ST } catch { Log "NOTIFY ERROR: $($_.Exception.Message)" }
  if ($resumes -ge $MaxResume) { exit 1 }
  $resumes++
  $p = Start-Process powershell.exe -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',"$D\diag22b.ps1" -WorkingDirectory $D -WindowStyle Hidden -PassThru
  $RunnerPid = $p.Id; Log "resume $resumes launched runner PID $RunnerPid"
}
