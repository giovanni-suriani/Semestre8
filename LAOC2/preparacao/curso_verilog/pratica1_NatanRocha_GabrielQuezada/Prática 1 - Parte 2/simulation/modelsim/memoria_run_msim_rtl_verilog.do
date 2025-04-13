transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+C:/Users/NATAN/Desktop/pratica1_NatanRocha_GabrielQuezada/Pr√°tica\ 1\ -\ Parte\ 2 {C:/Users/NATAN/Desktop/pratica1_NatanRocha_GabrielQuezada/Pr·tica 1 - Parte 2/memoria.v}
vlog -vlog01compat -work work +incdir+C:/Users/NATAN/Desktop/pratica1_NatanRocha_GabrielQuezada/Pr√°tica\ 1\ -\ Parte\ 2 {C:/Users/NATAN/Desktop/pratica1_NatanRocha_GabrielQuezada/Pr·tica 1 - Parte 2/ramlpm.v}
vlog -vlog01compat -work work +incdir+C:/Users/NATAN/Desktop/pratica1_NatanRocha_GabrielQuezada/Pr√°tica\ 1\ -\ Parte\ 2 {C:/Users/NATAN/Desktop/pratica1_NatanRocha_GabrielQuezada/Pr·tica 1 - Parte 2/disp7seg.v}

