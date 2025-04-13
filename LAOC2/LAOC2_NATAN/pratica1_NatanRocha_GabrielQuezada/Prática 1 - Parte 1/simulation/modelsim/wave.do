onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -label clock /ramlpm/clock
add wave -noupdate -label wren /ramlpm/wren
add wave -noupdate -label address -radix decimal /ramlpm/address
add wave -noupdate -label data -radix decimal /ramlpm/data
add wave -noupdate -label q -radix decimal /ramlpm/q
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ps} 0}
quietly wave cursor active 0
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ps} {346 ps}
view wave 
wave clipboard store
wave create -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 1000ps sim:/ramlpm/clock 
wave create -driver freeze -pattern clock -initialvalue 0 -period 250ps -dutycycle 50 -starttime 0ps -endtime 1000ps wren 
wave create -driver freeze -pattern repeater -initialvalue 1 -period 500ps -sequence { 1 100  } -repeat forever -range 4 0 -starttime 0ps -endtime 1000ps sim:/ramlpm/address 
WaveExpandAll -1
wave create -driver freeze -pattern repeater -initialvalue 111 -period 500ps -sequence { 111 100  } -repeat forever -range 7 0 -starttime 0ps -endtime 1000ps sim:/ramlpm/data 
WaveExpandAll -1
WaveCollapseAll -1
wave clipboard restore
