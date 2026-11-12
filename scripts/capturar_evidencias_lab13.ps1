# Ejecutar desde la RAIZ del repositorio en PowerShell.
$ErrorActionPreference = "Stop"
$python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "No existe .venv. Preparar el entorno antes." }
New-Item -ItemType Directory -Force -Path ".\docs" | Out-Null

Write-Host "[1/3] Ejecutando pruebas..."
& $python -m pytest -q 2>&1 | Tee-Object -FilePath ".\docs\lab13_braham_pytest.txt"
if ($LASTEXITCODE -ne 0) { throw "Pytest fallo. No subir evidencias como aprobadas." }

Write-Host "[2/3] Ejecutando Ruff..."
& $python -m ruff check . 2>&1 | Tee-Object -FilePath ".\docs\lab13_braham_ruff.txt"
if ($LASTEXITCODE -ne 0) { throw "Ruff fallo. Corregir antes de subir." }

Write-Host "[3/3] Registrando la rama y commits reales..."
"Rama actual:" | Out-File -Encoding utf8 ".\docs\lab13_braham_git.txt"
git branch --show-current | Out-File -Append -Encoding utf8 ".\docs\lab13_braham_git.txt"
"Ultimos 8 commits:" | Out-File -Append -Encoding utf8 ".\docs\lab13_braham_git.txt"
git log -8 --oneline | Out-File -Append -Encoding utf8 ".\docs\lab13_braham_git.txt"
Write-Host "EVIDENCIAS REALES CREADAS EN docs/: pytest, ruff, git."
