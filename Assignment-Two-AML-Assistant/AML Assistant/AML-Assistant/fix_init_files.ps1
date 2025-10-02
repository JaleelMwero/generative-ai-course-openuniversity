# fix_init_files.ps1
Write-Host "Fixing corrupted __init__.py files..." -ForegroundColor Cyan

$files = @(
    "src\__init__.py",
    "src\ai\__init__.py", 
    "src\core\__init__.py",
    "src\integration\__init__.py",
    "src\learning\__init__.py",
    "src\models\__init__.py",
    "src\simulation\__init__.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        # Create backup
        Copy-Item $file "$file.backup" -Force
        Write-Host "Backed up: $file" -ForegroundColor Yellow
        
        # Recreate with simple content
        Set-Content $file -Value "# Package initialization" -Encoding UTF8
        Write-Host "Fixed: $file" -ForegroundColor Green
    }
}

Write-Host "All files fixed!" -ForegroundColor Green
