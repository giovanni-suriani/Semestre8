module CTRL(OPcode,clock,MemRead,MemWrite,RegFonte,EscReg,RegOrdem2,PCouSalto,SaltoGeral,Branch,UlaFonte1,CtrlUla,Reset,RegOrdem1,RegOrdem3,ExtensorSinal,UlaFonte2);

input [3:0] OPcode;
input clock;
//Mudar UlaFOnte1 para apenas 1 bit
output reg MemRead,MemWrite,RegFonte,EscReg,RegOrdem2,PCouSalto,SaltoGeral,Branch,UlaFonte1,CtrlUla,Reset;
output reg[1:0]RegOrdem1,RegOrdem3,ExtensorSinal,UlaFonte2;

always @ (posedge clock) begin
casez(OPcode)
4'b111z: begin MemRead=1'b0; MemWrite=1'b0; RegFonte=1'b1;
EscReg = 1'b1; RegOrdem1 =2'bzz; RegOrdem2=1'bz; RegOrdem3=2'b10;
ExtensorSinal=2'b00; PCouSalto=1'b1; SaltoGeral=1'b0; Branch=1'b0;
UlaFonte1=1'b0; UlaFonte2=2'b01; CtrlUla=1'b0; Reset=1'b1;
end//set



4'b10zz: begin MemRead=1'b1; MemWrite=1'b0; RegFonte=1'b0;
EscReg = 1'b1; RegOrdem1 =2'b01; RegOrdem2=1'b0; RegOrdem3=2'b01;
ExtensorSinal=2'b10; PCouSalto=1'b1; SaltoGeral=1'b0; Branch=1'b0;
UlaFonte1=1'b1; UlaFonte2=2'b10; CtrlUla=1'b0; Reset=1'b1;
end//lw




4'b01zz: begin MemRead=1'b0; MemWrite=1'b1; RegFonte=1'b0;
EscReg = 1'b0; RegOrdem1 =2'b01; RegOrdem2=1'b0; RegOrdem3=2'b01;
ExtensorSinal=2'b10; PCouSalto=1'b1; SaltoGeral=1'b0; Branch=1'b0;
UlaFonte1=1'b1; UlaFonte2=2'b10; CtrlUla=1'b0; Reset=1'b1;
end//sw



4'b0000: begin MemRead=1'b0; MemWrite=1'b0; RegFonte=1'bz;
EscReg = 1'b0; RegOrdem1 =2'b00; RegOrdem2=1'b1; RegOrdem3=2'b00;
ExtensorSinal=2'bzz; PCouSalto=1'b0; SaltoGeral=1'b1; Branch=1'b1;
UlaFonte1=1'b0; UlaFonte2=2'b10; CtrlUla=1'b1; Reset=1'b1;
end//beq




4'b0001: begin MemRead=1'b0; MemWrite=1'b0; RegFonte=1'b1;
EscReg = 1'b1; RegOrdem1 =2'b00; RegOrdem2=1'b1; RegOrdem3=2'b00;
ExtensorSinal=2'bzz; PCouSalto=1'b1; SaltoGeral=1'b0; Branch=1'b0;
UlaFonte1=1'b0; UlaFonte2=2'b10; CtrlUla=1'b0; Reset=1'b1;
end//add




4'b0010: begin MemRead=1'b0; MemWrite=1'b0; RegFonte=1'b1;
EscReg = 1'b1; RegOrdem1 =2'b10; RegOrdem2=1'bz; RegOrdem3=2'b11;
ExtensorSinal=2'b10; PCouSalto=1'b1; SaltoGeral=1'b0; Branch=1'b0;
UlaFonte1=1'b1; UlaFonte2=2'b10; CtrlUla=1'b1; Reset=1'b1;
end//subi




4'b110z: begin MemRead=1'b0; MemWrite=1'b0; RegFonte=1'bz;
EscReg = 1'b0; RegOrdem1 =2'bzz; RegOrdem2=1'bz; RegOrdem3=2'bzz;
ExtensorSinal=2'b01; PCouSalto=1'b0; SaltoGeral=1'b1; Branch=1'b0;
UlaFonte1=1'bz; UlaFonte2=2'bzz; CtrlUla=1'bz; Reset=1'b1;
end//j




4'b0011: begin MemRead=1'b0; MemWrite=1'b0; RegFonte=1'bz;
EscReg = 1'b0; RegOrdem1 =2'bzz; RegOrdem2=1'bz; RegOrdem3=2'bzz;
ExtensorSinal=2'bzz; PCouSalto=1'b0; SaltoGeral=1'b0; Branch=1'bz;
UlaFonte1=1'bz; UlaFonte2=2'bzz; CtrlUla=1'bz; Reset=1'b0;
end//halt
endcase
end
endmodule
