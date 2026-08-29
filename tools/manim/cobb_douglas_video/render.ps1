# Render the full episode. Usage:
#   .\render.ps1            -> low quality preview (480p15) + stitch
#   .\render.ps1 -Final     -> 1080p30 final + stitch
# Renders to a LOCAL media dir (Google Drive sync locks the LaTeX/partial
# files if media lives on Y:), then copies the stitched mp4 back here.
param([switch]$Final)

$V = "Y:\Hunter\eco701\tools\manim\cobb_douglas_video"
$MediaLocal = Join-Path $env:LOCALAPPDATA "cd_video_media"
$mm = "$env:USERPROFILE\miniforge3\condabin\mamba.bat"
$env:PYTHONPATH = $V

if ($Final) {
    $flags = @("--resolution", "1920,1080", "--fps", "30")
    $qdir = "1080p30"
    $out = "episode1_cobb_douglas_1080p30.mp4"
} else {
    $flags = @("-ql")
    $qdir = "480p15"
    $out = "episode1_cobb_douglas_preview.mp4"
}

$scenes = @(
    @("s0_intro.py", "Intro"),
    @("s1_warmup.py", "Warmup1D"),
    @("s2_expression.py", "Expression"),
    @("s34_surface.py", "SurfaceToIsoquants"),
    @("s5_mrts.py", "MRTS"),
    @("s6_homothetic.py", "Homothetic"),
    @("s7_outro.py", "Outro")
)
foreach ($sc in $scenes) {
    & $mm run -n ecopy manim @flags "$V\$($sc[0])" $sc[1] --media_dir $MediaLocal
    if ($LASTEXITCODE -ne 0) { throw "render failed: $($sc[0])" }
}
& $mm run -n ecopy python "$V\stitch.py" $MediaLocal $qdir "$V\renders\$out"
Write-Host "done -> $V\renders\$out"
