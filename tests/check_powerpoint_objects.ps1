# Test only: inspect native objects and make reversible in-memory edits; never save.
param([Parameter(Mandatory=$true)][string]$Source)
$ErrorActionPreference='Stop'
$inputPath=(Resolve-Path -LiteralPath $Source).Path
$before=(Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash
$app=$null
$deck=$null
$counts=[ordered]@{slides=0; native_charts=0; native_tables=0; text_shapes=0; text_edit_test=$false; table_edit_test=$false; chart_edit_test=$false}
try {
    $app=New-Object -ComObject PowerPoint.Application
    $deck=$app.Presentations.Open($inputPath,-1,0,0)
    $counts.slides=$deck.Slides.Count
    foreach ($slide in $deck.Slides) {
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                $counts.text_shapes++
                if (-not $counts.text_edit_test) {
                    $original=$shape.TextFrame.TextRange.Text
                    $shape.TextFrame.TextRange.Text=$original+' synthetic edit test'
                    if (-not $shape.TextFrame.TextRange.Text.EndsWith(' synthetic edit test')) {throw 'Text edit failed'}
                    $shape.TextFrame.TextRange.Text=$original
                    $counts.text_edit_test=$true
                }
            }
            if ($shape.HasTable -eq -1) {
                $counts.native_tables++
                $cell=$shape.Table.Cell(1,1).Shape.TextFrame.TextRange
                $original=$cell.Text
                $cell.Text=$original+' synthetic edit test'
                if (-not $cell.Text.EndsWith(' synthetic edit test')) {throw 'Table edit failed'}
                $cell.Text=$original
                $counts.table_edit_test=$true
            }
            if ($shape.HasChart -eq -1) {
                $counts.native_charts++
                $series=$shape.Chart.SeriesCollection(1)
                $original=$series.Name
                $series.Name=$original+' synthetic edit test'
                if (-not $series.Name.EndsWith(' synthetic edit test')) {throw 'Chart series edit failed'}
                $series.Name=$original
                $counts.chart_edit_test=$true
            }
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($shape)
        }
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($slide)
    }
    $counts | ConvertTo-Json
} finally {
    if ($null -ne $deck) { $deck.Saved=-1; $deck.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($deck) }
    if ($null -ne $app) { [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) }
}
if ((Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash -ne $before) {throw 'Source was unexpectedly modified'}
if (-not $counts.text_edit_test -or -not $counts.table_edit_test -or -not $counts.chart_edit_test) {throw 'Expected synthetic fixture objects were not all tested'}
