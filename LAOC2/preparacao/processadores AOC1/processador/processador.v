module processador(clk, SBEQ);

wire [7:0] instrucao; 
wire reset;
input clk;
//clock c(clk);

//PC(clock, reset, enderecoE, enderecoS)

wire [7:0] enderecoS;
wire [7:0] enderecoE;

/*initial begin
 enderecoE = 8'b00000000; 
 reset = 1'b1;
end*/

PC pc(clk, reset, enderecoE, enderecoS);

//memoInst (leEndereco,instrucao,clock,reset);

memoInst memoi(enderecoS,instrucao,clk,reset);

//unidade de controle
//CTRL(OPcode,clock,MemRead,MemWrite,RegFonte,EscReg,RegOrdem2,PCouSalto,SaltoGeral,
//Branch,UlaFonte1,CtrlUla,Reset,RegOrdem1,RegOrdem3,ExtensorSinal,UlaFonte2);
wire MemRead,MemWrite,RegFonte,EscReg,RegOrdem2,PCouSalto,SaltoGeral,Branch,UlaFonte1,CtrlUla;
wire[1:0]RegOrdem1,RegOrdem3,ExtensorSinal,UlaFonte2;
wire [3:0] OPC;
assign OPC = instrucao[7:4]; 

CTRL controle(OPC,clk,MemRead,MemWrite,RegFonte,EscReg,RegOrdem2,PCouSalto,SaltoGeral,
Branch,UlaFonte1,CtrlUla,reset,RegOrdem1,RegOrdem3,ExtensorSinal,UlaFonte2);

//banco de registradores

//nomear fios 
wire [1:0] ro1_0;
assign ro1_0 = instrucao[1:0]; 
wire [1:0] ro1_1;
assign ro1_1 = instrucao[3:2];
wire [1:0] ro1_2;
assign ro1_2 = instrucao[3:2];  

//mux 3 entradas -- reg ordem1
//mux2bits3entradas(var1, var2, var3, sinal, saida);
wire [1:0]ro1_S;
mux2bits3entradas m2b3e(ro1_0, ro1_1, ro1_2, RegOrdem1, ro1_S);

//nomerar fios
wire [1:0] ro2_0;
assign ro2_0 = instrucao[5:4]; 
wire [1:0] ro2_1;
assign ro2_1 = instrucao[3:2];
//mux 2 entradas -- reg oredem2 
//mux2entradas(var1, var2, sinal, saida);
wire [1:0]ro2_S;
mux2entradas m2b2e(ro2_0, ro2_1, RegOrdem2, ro2_S);

//nomerar fios
wire [1:0] ro3_0;
assign ro3_0 = instrucao[3:2]; 
wire [1:0] ro3_1;
assign ro3_1 = instrucao[5:4];
wire [1:0] ro3_2;
assign ro3_2 = instrucao[4:3];
wire [1:0] ro3_3;
assign ro3_3 = instrucao[3:2];  

//mux 4 entradas -- regordem3
//mux2bits4entradas(var1, var2, var3, var4, sinal, saida);
wire [1:0]ro3_S;
mux2bits4entradas m2b4e(ro3_0, ro3_1, ro3_2, ro3_3, RegOrdem3, ro3_S);


//banco de registradores
//bancoDeReg (RegLido1,RegLido2,RegEscrito,DadoEscrito,EscReg,Dado1,Dado2,clock,reset,SBEQ);
wire [7:0] DadoEscritoR; 
wire [7:0] Dado1,Dado2;
output [7:0] SBEQ;
bancoDeReg br(ro1_S,ro2_S,ro3_S,DadoEscritoR,EscReg,Dado1,Dado2,clk,reset,SBEQ);

//extensores de sinal

//extensor 3 bits
wire [2:0] ES_3;
assign ES_3 = instrucao[2:0]; 
wire [7:0] ES_3S;
//extensor3bits(entrada,saida);
extensor3bits e3b(ES_3, ES_3S);

//extensor 5 bits
wire [4:0] ES_5;
assign ES_5 = instrucao[4:0]; 
wire [7:0] ES_5S;
extensor5bits e5b(ES_5, ES_5S);

//extendor 2 bits
wire [1:0] ES_2;
assign ES_2 = instrucao[1:0]; 
wire [7:0] ES_2S;
extensor2bits e2b(ES_2,ES_2S);

//mux extensor de sinal
//mux3ent8bits(var1, var2,var3, sinal, saida);
wire[7:0] ES_saida;
mux3ent8bits extSinal(ES_3S, ES_5S,ES_2S, ExtensorSinal, ES_saida);

//ulaFonte
//ula fonte 2
wire[7:0] UF2_S; // 
mux3ent8bits uf2(ES_saida, 8'b00000000, Dado2, UlaFonte2, UF2_S);

//ula fonte 1
wire[7:0] UF1_S; //
mux2ent8bits uf1(Dado1, ES_saida, UlaFonte1, UF1_S);

//ula
//ULAAOC(ctrlULA,num2,num1,zero,resultado);
wire zero; //
wire[7:0] resultado; //
ULAAOC ula(CtrlUla,UF2_S,UF1_S,zero,resultado);

//memoria de dados 
//memoDados(endereco,dadoEscrito,dadoLido,memRead,memWrite,clock,reset);
wire[7:0] dadoLido; //
memoDados md(resultado,Dado1,dadoLido,MemRead,MemWrite,clk,reset);

//mux regfonte
mux2ent8bits rf(dadoLido, resultado, RegFonte, DadoEscritoR);

//bancoDeReg br(ro1_S,ro2_S,ro3_S,DadoEscritoR,EscReg,Dado1,Dado2,clk,reset);

//and 
//PortaAND(entrada1,entrada2,saida);
wire S_and;
PortaAND pand(zero,Branch, S_and);

//mux saida da porta and
wire[7:0] S_tipoSalto;
mux2ent8bits tipoSalto(ES_saida, SBEQ, S_and, S_tipoSalto);

//salto geral
wire[7:0] S_saltoGeral;
mux2ent8bits tSaltoGegal(8'b00000000, S_tipoSalto, SaltoGeral, S_saltoGeral);

// adc 1
//somador(entrada1,entrada2,saida);
wire[7:0] S_adc1;
somador adc1(enderecoS,8'b00000001, S_adc1);

//pcousalto
wire[7:0] S_pcsalto;
mux2ent8bits mPcSalto(8'b00000000,  S_adc1, PCouSalto, S_pcsalto);

//adc 2
//wire[7:0] S_adc2;
somador adc2(S_saltoGeral,S_pcsalto, enderecoE);

/*
always@(*) begin
enderecoE = S_adc2;
end 
*/

always@(*) begin
$monitor("%8b ", SBEQ);
end
endmodule
