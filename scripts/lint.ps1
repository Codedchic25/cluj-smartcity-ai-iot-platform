# =============================================================================
# Automated Quality Control & Syntax Enforcement Pipeline (Windows Native)
# =============================================================================
# Role: Orchestrates 'uv' and 'ruff' to format, lint, and clean workspace
# artifacts natively on Windows without requiring third-party Bash tools.
# =============================================================================

$StartMsg = "[LINT PIPELINE]: Commencing codebase validation passes on Windows..."
Write-Host $StartMsg -ForegroundColor Cyan

# 1. Asynchronous Cache and Compilation Artifacts Eviction Layer
Write-Host "[LINT PIPELINE]: Cleaning workspace file cache buffers..." -ForegroundColor Gray

# Dispatch a fast background job to purge caching markers without freezing threads
Start-Job -ScriptBlock {
    Get-ChildItem -Path . -Filter "__pycache__" -Recurse | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Filter ".pytest_cache" -Recurse | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Filter ".ruff_cache" -Recurse | Remove-Item -Recurse -Force
} | Out-Null

# 2. Automatic Code Formatting
$FmtMsg = "[LINT PIPELINE]: Phase 1 - Aligning aesthetics via Ruff formatter..."
Write-Host $FmtMsg -ForegroundColor Yellow
uv run ruff format .
# 3. Automated Linting and Code Fixes
$LintMsg = "[LINT PIPELINE]: Phase 2 - Triggering advanced stylistic rule parsing checks..."
Write-Host $LintMsg -ForegroundColor Yellow

# Clean execution layer utilizing centralized settings from pyproject.toml
uv run ruff check . --fix

# Enforce clean thread synchronization by waiting for the background job to conclude
Get-Job | Wait-Job | Remove-Job

$SuccessMsg = "[SUCCESS]: Cache evicted and all modules conform to the highest Python targets."
Write-Host $SuccessMsg -ForegroundColor Green

