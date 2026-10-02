$ErrorActionPreference = "Continue"
Set-Location "C:\Users\Akitt\Grok\worktree-mhd\ns"
$env:PYTHONPATH = "C:\Users\Akitt\Grok\worktree-mhd\ns"
$env:JAX_PLATFORMS = "cpu"
$env:PYTHONUNBUFFERED = "1"
$py = "C:\Users\Akitt\Grok\.venv\Scripts\python.exe"
$outLog = "C:\Users\Akitt\Grok\worktree-mhd\ns\examples\section_A_crank_console.log"
$errLog = "C:\Users\Akitt\Grok\worktree-mhd\ns\examples\section_A_crank_console.err"
"START $(Get-Date -Format o) pid=$PID" | Out-File $outLog -Encoding utf8
& $py -u .\examples\run_section_A.py --crank --N 32 --t-end 2 --nu-fac 8 --d-i 0.2 *>> $outLog 2>> $errLog
$code = $LASTEXITCODE
"END $(Get-Date -Format o) exit=$code" | Out-File $outLog -Append -Encoding utf8
