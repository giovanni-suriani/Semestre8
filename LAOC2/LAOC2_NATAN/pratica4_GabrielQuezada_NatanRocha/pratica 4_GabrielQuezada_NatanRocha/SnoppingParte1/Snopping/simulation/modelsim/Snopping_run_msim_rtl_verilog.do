transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+C:/Users/NATAN/Downloads/Pratica\ 4_GabrielQuezada_NatanRocha/SnoppingParte1/SnoppingParte1/Snopping {C:/Users/NATAN/Downloads/Pratica 4_GabrielQuezada_NatanRocha/SnoppingParte1/SnoppingParte1/Snopping/Snopping.v}
vlog -vlog01compat -work work +incdir+C:/Users/NATAN/Downloads/Pratica\ 4_GabrielQuezada_NatanRocha/SnoppingParte1/SnoppingParte1/Snopping {C:/Users/NATAN/Downloads/Pratica 4_GabrielQuezada_NatanRocha/SnoppingParte1/SnoppingParte1/Snopping/Receptor.v}
vlog -vlog01compat -work work +incdir+C:/Users/NATAN/Downloads/Pratica\ 4_GabrielQuezada_NatanRocha/SnoppingParte1/SnoppingParte1/Snopping {C:/Users/NATAN/Downloads/Pratica 4_GabrielQuezada_NatanRocha/SnoppingParte1/SnoppingParte1/Snopping/Emissor.v}

vlog -vlog01compat -work work +incdir+C:/Users/NATAN/Downloads/Pratica\ 4_GabrielQuezada_NatanRocha/SnoppingParte1/SnoppingParte1/Snopping {C:/Users/NATAN/Downloads/Pratica 4_GabrielQuezada_NatanRocha/SnoppingParte1/SnoppingParte1/Snopping/ReceptorTestbench.v}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cycloneii_ver -L rtl_work -L work -voptargs="+acc"  ReceptorTestbench

add wave *
view structure
view signals
run -all
