onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -color Gold -itemcolor Gold /SnoppingTestbench/u_Snopping/u_C0/r_Memory
add wave -noupdate -color Red -itemcolor Red /SnoppingTestbench/u_Snopping/u_C1/r_Memory
add wave -noupdate -color Blue -itemcolor Blue /SnoppingTestbench/u_Snopping/u_C3/r_Memory
add wave -noupdate /SnoppingTestbench/u_Snopping/u_Memory/r_Memory
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {66 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ps
update
WaveRestoreZoom {0 ps} {1 ns}
