$ErrorActionPreference='Continue'; Set-Location C:\Users\Akitt\Grok\jobs\instanton-tests
$Py='C:\Users\Akitt\Grok\.venv\Scripts\python.exe'; $ST='logs\diag22b\bpst_status.txt'; $LOG='logs\diag22b\bpst_prestep.log'; $GF='out\diag22b\bpst_prestep.json'
Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} BST start it1b-bpst" -f (Get-Date)); $t0=Get-Date
$wj=Start-Job { param($ST) while($true){ Start-Sleep 60; $f=(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB; Add-Content $ST ("{0:HH:mm:ss} alive freeGB {1:N1}" -f (Get-Date),$f) } } -ArgumentList (Resolve-Path $ST).Path
$p=Start-Process $Py -ArgumentList '-u','run.py','it1b-bpst' -RedirectStandardOutput $LOG -RedirectStandardError 'logs\diag22b\bpst_prestep.err' -NoNewWindow -Wait -PassThru
Stop-Job $wj; Remove-Job $wj
$ec=$p.ExitCode; $fresh=(Test-Path $GF) -and ((Get-Item $GF).LastWriteTime -ge $t0)
$st = if(-not $fresh){'CRASH'} elseif($null -eq $ec -or "$ec" -eq ''){'UNKNOWN'} elseif($ec -eq 0){'PASS'} elseif($ec -eq 3){'FAIL'} else {'CRASH'}
$ecs = if($null -eq $ec -or "$ec" -eq ''){'unknown'} else {"$ec"}
Add-Content $ST ("{0:yyyy-MM-dd HH:mm:ss} end exit {1} {2} grade_file_fresh={3}" -f (Get-Date),$ecs,$st,$fresh)
try{ & C:\Users\Akitt\Grok\jobs\notify.ps1 -Status $st -Summary "IT1b BPST pre-step finished: $st (exit $ecs); $GF" -GradeFile $GF -StatusFile $ST }catch{ Add-Content $ST "NOTIFY ERROR $($_.Exception.Message)" }
