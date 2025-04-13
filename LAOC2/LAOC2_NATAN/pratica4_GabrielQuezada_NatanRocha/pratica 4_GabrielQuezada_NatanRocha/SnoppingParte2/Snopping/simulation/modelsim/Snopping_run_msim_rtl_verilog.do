transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+C:/Users/guilh/Downloads/Snopping/Snopping {C:/Users/guilh/Downloads/Snopping/Snopping/Snopping.v}
vlog -vlog01compat -work work +incdir+C:/Users/guilh/Downloads/Snopping/Snopping {C:/Users/guilh/Downloads/Snopping/Snopping/Cache.v}
vlog -vlog01compat -work work +incdir+C:/Users/guilh/Downloads/Snopping/Snopping {C:/Users/guilh/Downloads/Snopping/Snopping/Bus.v}
vlog -vlog01compat -work work +incdir+C:/Users/guilh/Downloads/Snopping/Snopping {C:/Users/guilh/Downloads/Snopping/Snopping/Memory.v}

vlog -vlog01compat -work work +incdir+C:/Users/guilh/Downloads/Snopping/Snopping {C:/Users/guilh/Downloads/Snopping/Snopping/SnoppingTestbench.v}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cycloneii_ver -L rtl_work -L work -voptargs="+acc"  SnoppingTestbench

add wave *
view structure
view signals
run -all
