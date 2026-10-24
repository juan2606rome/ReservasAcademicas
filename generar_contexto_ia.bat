@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$root='%~dp0'; $s=[IO.File]::ReadAllText('%~f0'); $i=$s.IndexOf(([string][char]10)+'#PS#'); Invoke-Expression $s.Substring($i)"
pause
exit /b
#PS#
# ===================== CONFIGURACION =====================
$maxKB     = 300     # solo se omiten archivos de texto mayores a esto (y se avisa)
$compactar = $true   # quita espacios al final y lineas en blanco repetidas

# Si NO esta vacia, solo se incluye el CONTENIDO de los archivos que coincidan
# (el arbol siempre muestra todo). Rutas relativas con /, comodin *.
# Ejemplo: $soloRutas = 'app/src/main/java/com/pandasz/clientevr/mando/vio/*','rust-lib/src/*'
$soloRutas = @()

# Rutas a excluir del contenido (siguen apareciendo en el arbol)
# Ejemplo: $excluirRutas = 'PLAN_VIO_TIPO_ARCORE.md','MAPA_PROYECTO.md'
$excluirRutas = @()

# Carpetas que NO se recorren (generadas, temporales o pesadas)
$excDirs = 'build','target','.gradle','.idea','.kotlin','.vscode','.git','node_modules','__pycache__','.venv','ALVR'

# Archivos ignorados por nombre
$excFiles = '*.lock','crash*.txt','log*.txt','local.properties','gradlew','gradlew.bat','generar_contexto_ia.bat','PROYECTO_PARA_IA*.txt'

# Extensiones binarias (nunca se incluyen)
$extBinarias = '.png','.jpg','.jpeg','.webp','.gif','.ico','.jar','.class','.so','.a','.o','.apk','.aab','.zip','.bin','.tflite','.task','.onnx','.ttf','.otf','.woff','.mp4','.mp3','.wav','.pdf','.dll','.exe','.rlib','.rmeta','.pdb','.jks','.keystore'
# =========================================================

$root = $root.TrimEnd('\')
$out  = Join-Path $root 'PROYECTO_PARA_IA.txt'
$utf8 = New-Object System.Text.UTF8Encoding($false)
$tree  = New-Object System.Collections.Generic.List[string]
$files = New-Object System.Collections.Generic.List[object]

function Coincide($rel, $patrones) {
    foreach ($p in $patrones) { if ($rel -like $p) { return $true } }
    return $false
}

function Walk($path, $indent) {
    $items = Get-ChildItem -LiteralPath $path -Force | Sort-Object @{e={-not $_.PSIsContainer}}, Name
    foreach ($it in $items) {
        if ($it.PSIsContainer) {
            if ($excDirs -contains $it.Name) { continue }
            $tree.Add("${indent}$($it.Name)/")
            Walk $it.FullName ($indent + '  ')
        } else {
            if (Coincide $it.Name $excFiles) { continue }
            if ($extBinarias -contains $it.Extension.ToLower()) { continue }
            $tree.Add("${indent}$($it.Name)")
            $files.Add($it)
        }
    }
}

function Compactar($t) {
    $t = $t -replace "`r`n", "`n"
    $t = $t -replace "[ \t]+`n", "`n"
    $t = $t -replace "`n{3,}", "`n`n"
    return $t.Trim()
}

Walk $root ''

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("<project name=""$(Split-Path $root -Leaf)"">")
[void]$sb.AppendLine('<directory_tree>')
foreach ($l in $tree) { [void]$sb.AppendLine($l) }
[void]$sb.AppendLine('</directory_tree>')
[void]$sb.AppendLine('<files>')

$omitidos  = @()
$binarios  = @()
$incluidos = @()
foreach ($f in $files) {
    $rel = $f.FullName.Substring($root.Length + 1).Replace('\','/')
    if ($soloRutas.Count -gt 0 -and -not (Coincide $rel $soloRutas)) { continue }
    if (Coincide $rel $excluirRutas) { continue }
    if ($f.Length -gt ($maxKB * 1KB)) { $omitidos += $f; continue }

    $bytes = [IO.File]::ReadAllBytes($f.FullName)
    $n = [math]::Min($bytes.Length, 2000)
    $bin = $false
    for ($k = 0; $k -lt $n; $k++) { if ($bytes[$k] -eq 0) { $bin = $true; break } }
    if ($bin) { $binarios += $rel; continue }

    $txt = [Text.Encoding]::UTF8.GetString($bytes).TrimStart([char]0xFEFF)
    if ($compactar) { $txt = Compactar $txt }
    [void]$sb.AppendLine("<file path=""$rel"">")
    [void]$sb.AppendLine($txt)
    [void]$sb.AppendLine('</file>')
    $incluidos += [pscustomobject]@{ Ruta = $rel; Chars = $txt.Length }
}

[void]$sb.AppendLine('</files>')
[void]$sb.AppendLine('</project>')
[IO.File]::WriteAllText($out, $sb.ToString(), $utf8)

$chars  = $sb.Length
$tokens = [math]::Round($chars / 3.5)
Write-Host ""
Write-Host "Listo: $out" -ForegroundColor Green
Write-Host "Archivos incluidos: $($incluidos.Count)  |  Caracteres: $chars  |  Tokens aprox: $tokens"
if ($tokens -gt 150000) {
    Write-Host "AVISO: es muy grande y puede no caber en el contexto. Usa `$soloRutas o `$excluirRutas." -ForegroundColor Red
}
Write-Host ""
Write-Host "Los 8 mas pesados:" -ForegroundColor Yellow
$incluidos | Sort-Object Chars -Descending | Select-Object -First 8 | ForEach-Object {
    Write-Host ("  {0,8} chars  {1}" -f $_.Chars, $_.Ruta)
}
if ($omitidos.Count -gt 0) {
    Write-Host ""
    Write-Host "OMITIDOS por superar $maxKB KB:" -ForegroundColor Red
    $omitidos | ForEach-Object { Write-Host "  $($_.Name)  ($([math]::Round($_.Length/1KB)) KB)" }
}
if ($binarios.Count -gt 0) {
    Write-Host ""
    Write-Host "Omitidos por ser binarios:" -ForegroundColor Yellow
    $binarios | ForEach-Object { Write-Host "  $_" }
}
