# Portable read-only PowerPoint rendering. Close only the presentation opened here.
param(
    [Parameter(Mandatory=$true)][string]$Source,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [int[]]$Slides = @(),
    [ValidateRange(320,3840)][int]$Width = 1920
)
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $Source).Path
$renderPath = [System.IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $renderPath) { throw 'Use a new render directory; stale PNGs cannot count as validation.' }
New-Item -ItemType Directory -Path $renderPath | Out-Null
$inputHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
$app = $null
$deck = $null
$rendered = @()
try {
    $app = New-Object -ComObject PowerPoint.Application
    $deck = $app.Presentations.Open($sourcePath, -1, 0, 0)
    $height = [int][Math]::Round($Width * $deck.PageSetup.SlideHeight / $deck.PageSetup.SlideWidth)
    if ($Slides.Count -eq 0) { $Slides = @(1..$deck.Slides.Count) }
    foreach ($index in $Slides) {
        if ($index -lt 1 -or $index -gt $deck.Slides.Count) { throw 'Slide index outside presentation' }
        $slide = $null
        try {
            $slide = $deck.Slides.Item($index)
            $image = Join-Path $renderPath ('slide-{0:D3}.png' -f $index)
            $slide.Export($image, 'PNG', $Width, $height)
            $rendered += [ordered]@{slide=$index; image=[System.IO.Path]::GetFileName($image); hidden=($slide.SlideShowTransition.Hidden -eq -1)}
        } finally {
            if ($null -ne $slide) { [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($slide) }
        }
    }
    $result = [ordered]@{source_sha256=$inputHash; renderer='Microsoft PowerPoint Slide.Export'; version=$app.Version; slide_count=$deck.Slides.Count; width=$Width; height=$height; slides=$rendered; visual_status='unreviewed'; animation_playback='not_tested'}
    $result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $renderPath 'render-manifest.json') -Encoding UTF8
    Write-Output ("Rendered {0} slides; visual review still required." -f $rendered.Count)
} finally {
    if ($null -ne $deck) { $deck.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($deck) }
    if ($null -ne $app) { [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) }
    # Never Quit: the application may host unrelated user presentations.
}
if ((Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $inputHash) { throw 'Source changed during rendering. Do not reuse this review.' }
