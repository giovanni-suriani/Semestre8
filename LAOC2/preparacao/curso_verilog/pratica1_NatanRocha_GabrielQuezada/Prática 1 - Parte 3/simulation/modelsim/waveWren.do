view wave 
wave clipboard store
wave create -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 1000ps sim:/Cache/clock 
wave create -driver freeze -pattern repeater -initialvalue 10110 -period 50ps -sequence { 10110  } -repeat forever -range 4 0 -starttime 0ps -endtime 1000ps sim:/Cache/address 
WaveExpandAll -1
wave create -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 500ps -endtime 1000ps sim:/Cache/wren 
wave modify -driver freeze -pattern clock -initialvalue St0 -period 250ps -dutycycle 50 -starttime 500ps -endtime 1000ps Edit:/Cache/wren 
wave modify -driver freeze -pattern clock -initialvalue St0 -period 250ps -dutycycle 25 -starttime 500ps -endtime 1000ps Edit:/Cache/wren 
wave modify -driver freeze -pattern clock -initialvalue St0 -period 100ps -dutycycle 75 -starttime 500ps -endtime 1000ps Edit:/Cache/wren 
wave modify -driver freeze -pattern constant -value 1 -starttime 500ps -endtime 1000ps Edit:/Cache/wren 
wave create -driver freeze -pattern repeater -initialvalue 111 -period 50ps -sequence { 111  } -repeat forever -range 7 0 -starttime 500ps -endtime 1000ps sim:/Cache/data 
WaveExpandAll -1
WaveCollapseAll -1
wave clipboard restore
