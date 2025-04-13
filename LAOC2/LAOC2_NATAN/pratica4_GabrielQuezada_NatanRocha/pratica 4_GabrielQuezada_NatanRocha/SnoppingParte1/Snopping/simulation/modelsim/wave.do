onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -color Red -itemcolor Red -radix unsigned -childformat {{{/SnoppingTestbench/u_Dut/u_Emissor/i_Operation[1]} -radix unsigned} {{/SnoppingTestbench/u_Dut/u_Emissor/i_Operation[0]} -radix unsigned}} -expand -subitemconfig {{/SnoppingTestbench/u_Dut/u_Emissor/i_Operation[1]} {-color Red -itemcolor Red -radix unsigned} {/SnoppingTestbench/u_Dut/u_Emissor/i_Operation[0]} {-color Red -itemcolor Red -radix unsigned}} /SnoppingTestbench/u_Dut/u_Emissor/i_Operation
add wave -noupdate -color Red -itemcolor Red -radix unsigned -childformat {{{/SnoppingTestbench/u_Dut/u_Emissor/r_State[1]} -radix unsigned} {{/SnoppingTestbench/u_Dut/u_Emissor/r_State[0]} -radix unsigned}} -expand -subitemconfig {{/SnoppingTestbench/u_Dut/u_Emissor/r_State[1]} {-color Red -itemcolor Red -radix unsigned} {/SnoppingTestbench/u_Dut/u_Emissor/r_State[0]} {-color Red -itemcolor Red -radix unsigned}} /SnoppingTestbench/u_Dut/u_Emissor/r_State
add wave -noupdate -color Red -itemcolor Red -radix unsigned /SnoppingTestbench/u_Dut/u_Emissor/r_Message
add wave -noupdate -color Red -itemcolor Red -radix unsigned -childformat {{{/SnoppingTestbench/u_Dut/u_Emissor/r_Action[1]} -radix unsigned} {{/SnoppingTestbench/u_Dut/u_Emissor/r_Action[0]} -radix unsigned}} -expand -subitemconfig {{/SnoppingTestbench/u_Dut/u_Emissor/r_Action[1]} {-color Red -itemcolor Red -radix unsigned} {/SnoppingTestbench/u_Dut/u_Emissor/r_Action[0]} {-color Red -itemcolor Red -radix unsigned}} /SnoppingTestbench/u_Dut/u_Emissor/r_Action
add wave -noupdate -color Gold -itemcolor Gold -radix unsigned -childformat {{{/SnoppingTestbench/u_Dut/u_Receptor/i_Message[1]} -radix unsigned} {{/SnoppingTestbench/u_Dut/u_Receptor/i_Message[0]} -radix unsigned}} -expand -subitemconfig {{/SnoppingTestbench/u_Dut/u_Receptor/i_Message[1]} {-color Gold -itemcolor Gold -radix unsigned} {/SnoppingTestbench/u_Dut/u_Receptor/i_Message[0]} {-color Gold -itemcolor Gold -radix unsigned}} /SnoppingTestbench/u_Dut/u_Receptor/i_Message
add wave -noupdate -color Gold -itemcolor Gold -radix unsigned -childformat {{{/SnoppingTestbench/u_Dut/u_Receptor/r_State[1]} -radix unsigned} {{/SnoppingTestbench/u_Dut/u_Receptor/r_State[0]} -radix unsigned}} -expand -subitemconfig {{/SnoppingTestbench/u_Dut/u_Receptor/r_State[1]} {-color Gold -itemcolor Gold -radix unsigned} {/SnoppingTestbench/u_Dut/u_Receptor/r_State[0]} {-color Gold -itemcolor Gold -radix unsigned}} /SnoppingTestbench/u_Dut/u_Receptor/r_State
add wave -noupdate -color Gold -itemcolor Gold -radix unsigned -childformat {{{/SnoppingTestbench/u_Dut/u_Receptor/r_Signal[1]} -radix unsigned} {{/SnoppingTestbench/u_Dut/u_Receptor/r_Signal[0]} -radix unsigned}} -expand -subitemconfig {{/SnoppingTestbench/u_Dut/u_Receptor/r_Signal[1]} {-color Gold -itemcolor Gold -radix unsigned} {/SnoppingTestbench/u_Dut/u_Receptor/r_Signal[0]} {-color Gold -itemcolor Gold -radix unsigned}} /SnoppingTestbench/u_Dut/u_Receptor/r_Signal
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {307 ps} 0}
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
