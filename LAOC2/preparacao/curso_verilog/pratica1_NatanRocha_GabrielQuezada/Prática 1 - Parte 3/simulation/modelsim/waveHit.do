onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -label Clock /Cache/clock
add wave -noupdate -label Address /Cache/address
add wave -noupdate -label Hit /Cache/hit
add wave -noupdate -label q -radix decimal /Cache/q
add wave -noupdate -label Cache -expand -subitemconfig {{/Cache/cache[1]} -expand {/Cache/cache[0]} -expand} /Cache/cache
add wave -noupdate -label State -radix decimal /Cache/state
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
WaveRestoreZoom {0 ps} {2 ns}
view wave 
wave clipboard store
wave create -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 1000ps clock 
wave create -driver freeze -pattern repeater -initialvalue 100 -period 50ps -sequence { 100  } -repeat forever -range 4 0 -starttime 0ps -endtime 1000ps sim:/Cache/address 
WaveExpandAll -1
WaveCollapseAll -1
wave clipboard restore
