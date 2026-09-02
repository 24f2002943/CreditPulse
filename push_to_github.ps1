$env:Path = "C:\Users\VRUNDA\tools\git\cmd;C:\Users\VRUNDA\tools\nodejs;C:\Users\VRUNDA\tools\uv;$env:Path"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Pushing CreditPulse to GitHub (main)   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSUCCESS! Your repository is now updated on GitHub: https://github.com/24f2002943/CreditPulse" -ForegroundColor Green
} else {
    Write-Host "`nPush encountered an issue. Check the output above." -ForegroundColor Yellow
}
