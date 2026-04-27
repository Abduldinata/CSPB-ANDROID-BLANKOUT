$ErrorActionPreference='Stop'
function Set-CoordsPreserveCmd {
  param([string]$file,[hashtable]$map)
  $lines = Get-Content -Path $file
  $changed = $false
  for($i=0;$i -lt $lines.Count;$i++){
    $line = $lines[$i]
    foreach($id in $map.Keys){
      $pat = '^(\s*touch_addbutton\s+"' + [regex]::Escape($id) + '"\s+""\s+"[^"]*"\s+).*$'
      if($line -match $pat){
        $lines[$i] = ($matches[1] + $map[$id])
        $changed = $true
        break
      }
    }
  }
  if($changed){ Set-Content -Path $file -Value $lines -Encoding ASCII }
  return $changed
}

$globalMap1 = @{ 'lobby_enter1'='0.887500 0.838889 0.937500 0.905556 255 255 255 255 6'; '_lobby_enter1'='0.887500 0.838889 0.937500 0.905556 255 255 255 255 6'; '_lobby_enter1_2'='0.887500 0.838889 0.937500 0.905556 255 255 255 255 6'; 'lobby_enter1_2'='0.887500 0.838889 0.937500 0.905556 255 255 255 255 6'; '_lobby_out'='0.940625 0.937500 0.982031 0.993056 255 255 255 255 6' }
$globalMap2 = @{ '_lobby_back1'='0.634375 0.762500 0.677344 0.823611 255 255 255 255 6'; '_lobby_enter2'='0.805469 0.766667 0.847656 0.823611 255 255 255 255 6'; '_lobby_out2'='0.940625 0.937500 0.982031 0.993056 255 255 255 255 6'; '_lobby_notice_1'='0.070312 0.787500 0.137500 0.812500 255 255 255 255 6'; '_lobby_notice_2'='0.143750 0.787500 0.210938 0.812500 255 255 255 255 6'; '_lobby_notice_3'='0.215625 0.787500 0.282813 0.812500 255 255 255 255 6' }
$globalMap3 = @{ '_lobby_back2'='0.729688 0.822222 0.770312 0.875000 255 255 255 255 6'; '_lobby_enter3'='0.784375 0.822222 0.825000 0.875000 255 255 255 255 6'; '_lobby_out3'='0.939063 0.938889 0.979688 0.995833 255 255 255 255 6' }
$globalMap4 = @{ '_lobby_changeteam1'='0.390625 0.843056 0.457813 0.902778 255 255 255 255 6'; '_lobby_back3'='0.729688 0.822222 0.770312 0.875000 255 255 255 255 6'; '_lobby_enter4'='0.784375 0.822222 0.825000 0.875000 255 255 255 255 6'; '_lobby_out4'='0.939063 0.938889 0.979688 0.995833 255 255 255 255 6' }
$suffixMap = @{ '_lobby_credit'='0.611719 0.941667 0.650781 0.993056 255 255 255 255 6'; '_lobby_choose'='0.527344 0.820833 0.608594 0.870833 255 255 255 255 6'; '_lobby_inventory1'='0.745313 0.941667 0.784375 0.997222 255 255 255 255 6'; '_lobby_friend1'='0.835938 0.938889 0.876563 0.995833 255 255 255 255 6'; '_lobby_friend2'='0.815625 0.879167 0.875781 0.916667 255 255 255 255 6'; '_lobby_mission1'='0.701562 0.941667 0.740625 0.997222 255 255 255 255 6'; '_lobby_clan1'='0.656250 0.941667 0.695312 0.997222 255 255 255 255 6'; '_lobby_back2'='0.729688 0.822222 0.770312 0.875000 255 255 255 255 6'; '_lobby_enter3'='0.784375 0.822222 0.825000 0.875000 255 255 255 255 6'; '_lobby_out3'='0.939063 0.938889 0.979688 0.995833 255 255 255 255 6' }
$classMap = @{ '_lobby_start_blue1'='0.828906 0.847222 0.893750 0.897222 255 255 255 255 6'; '_lobby_start_red1'='0.828906 0.847222 0.893750 0.897222 255 255 255 255 6'; '_lobby_back3'='0.905469 0.847222 0.970313 0.897222 255 255 255 255 6'; '_lobby_detail'='0.010937 0.900000 0.367969 0.940278 255 255 255 255 6'; '_lobby_detail1'='0.010937 0.900000 0.367969 0.940278 255 255 255 255 6'; '_lobby_detail2'='0.010937 0.580556 0.367969 0.620833 255 255 255 255 6'; '_select_open_mapf'='0.531250 0.533333 0.554688 0.556944 255 255 255 255 6'; '_select_close_mapf'='0.531250 0.533333 0.554688 0.556944 255 255 255 255 6'; '_mode_tdm'='0.562500 0.488889 0.584375 0.515278 255 255 255 255 6'; '_mode_bm'='0.687500 0.488889 0.709375 0.515278 255 255 255 255 6' }

$changed=0
if(Set-CoordsPreserveCmd "files/cspb/addons/neda/default/lobby_menu.cfg" $globalMap1){$changed++}
if(Set-CoordsPreserveCmd "files/cspb/addons/neda/default/lobby_menu2.cfg" $globalMap2){$changed++}
if(Set-CoordsPreserveCmd "files/cspb/addons/neda/default/lobby_menu3.cfg" $globalMap3){$changed++}
if(Set-CoordsPreserveCmd "files/cspb/addons/neda/default/lobby_menu4.cfg" $globalMap4){$changed++}
$suffixFiles = Get-ChildItem "files/cspb/addons/neda/blueteam" -Directory | ForEach-Object { Join-Path $_.FullName "lobby_menu3.cfg" }
$suffixFiles += Get-ChildItem "files/cspb/addons/neda/redteam" -Directory | ForEach-Object { Join-Path $_.FullName "lobby_menu3.cfg" }
foreach($f in $suffixFiles){ if(Test-Path $f){ if(Set-CoordsPreserveCmd $f $suffixMap){$changed++} } }
$classFiles = Get-ChildItem "files/cspb/addons/neda/team" -Filter "team_*_class*.cfg" | Select-Object -ExpandProperty FullName
foreach($f in $classFiles){ if(Set-CoordsPreserveCmd $f $classMap){$changed++} }
"coord_files_changed=$changed"
