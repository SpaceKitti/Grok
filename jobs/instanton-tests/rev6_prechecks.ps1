# IT1b rev 6 (E360229B) staged pre-checks C1+C2 under eps=-1 (Aethon 2026-10-23). STOPS before any delta row. Reduced model.
# Launcher logic per E844D5DC: Start-Process -Wait -PassThru; blank exit = UNKNOWN; CRASH only on non-zero (non-3) exit or missing/stale output.
$ErrorActionPreference='Continue'; Set-Location C:\Users\Akitt\Grok\jobs\instanton-tests
$Py=(Get-Content python_path.txt).Trim(); $L='logs\diag22b\rev6'; New-Item -ItemType Directory $L -Force | Out-Null
$ST="$L\rev6_status.txt"; $Notify='C:\Users\Akitt\Grok\jobs\notify.ps1'
function Log($m){ Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} BST {1}" -f (Get-Date),$m) }
function Grade($p,$out,$t0){ $ec=$p.ExitCode; $fresh=(Test-Path $out) -and ((Get-Item $out).LastWriteTime -ge $t0)
  $st= if(-not $fresh){'CRASH'} elseif($null -eq $ec -or "$ec" -eq ''){'UNKNOWN'} elseif($ec -eq 0){'PASS'} elseif($ec -eq 3){'FAIL'} else {'CRASH'}
  $ecs= if($null -eq $ec -or "$ec" -eq ''){'unknown'} else {"$ec"}; return @($st,$ecs) }
function Run($tag,$argl,$out){ $t0=Get-Date; Log "start $tag"
  $p=Start-Process $Py -ArgumentList (@('-u','run.py')+$argl) -RedirectStandardOutput "$L\$tag.log" -RedirectStandardError "$L\$tag.err" -NoNewWindow -Wait -PassThru
  $g=Grade $p $out $t0; Log ("end {0} exit {1} {2} wall_s {3:N0}" -f $tag,$g[1],$g[0],((Get-Date)-$t0).TotalSeconds); return $g[0] }
function Note($st,$m){ try{ & $Notify -Status $st -Summary $m -StatusFile $ST }catch{ Log "NOTIFY ERROR $($_.Exception.Message)" } }
Log "rev6 prechecks begin (runner PID $PID)"
$c=Run 'C1_cal' @('it1b-cal') 'out\diag22b\cal_B10_eps-1.json'
if($c -ne 'PASS'){ Log "STOP after C1: $c"; Note $c "IT1b rev6 C1 calibration eps=-1: $c; stopped before C2"; exit 1 }
$jobs=@(); $t0=Get-Date; Log "start C2 (bpst + X0 a1.0 + X0 a0.5, parallel)"
foreach($a in @(@('C2_bpst',@('it1b-bpst','--eps','-1'),'out\diag22b\bpst_prestep_eps-1.json'),@('C2_x0_a1.0',@('it1b-x0','--alpha','1.0'),'out\diag22b\rows_rev6\B10_a1.0_s-1_delta0.0.json'),@('C2_x0_a0.5',@('it1b-x0','--alpha','0.5'),'out\diag22b\rows_rev6\B10_a0.5_s-1_delta0.0.json'))){
  $p=Start-Process $Py -ArgumentList (@('-u','run.py')+$a[1]) -RedirectStandardOutput "$L\$($a[0]).log" -RedirectStandardError "$L\$($a[0]).err" -NoNewWindow -PassThru
  $null=$p.Handle; $jobs+=,@($a[0],$p,$a[2]) }
$all='PASS'; foreach($j in $jobs){ $j[1].WaitForExit(); $g=Grade $j[1] $j[2] $t0; Log ("end {0} exit {1} {2} wall_s {3:N0}" -f $j[0],$g[1],$g[0],($j[1].ExitTime-$j[1].StartTime).TotalSeconds); if($g[0] -ne 'PASS'){ $all=$g[0] } }
Log "rev6 prechecks DONE C1 PASS, C2 $all; STOPPED before delta rows (held for Venus review)"
Note $all "IT1b rev6 prechecks: C1 PASS, C2 $all; no delta rows launched"
