module bancoDeReg (RegLido1,RegLido2,RegEscrito,DadoEscrito,EscReg,Dado1,Dado2,clock,reset,SBEQ);
input [1:0] RegLido1,RegLido2,RegEscrito; 
input EscReg,clock,reset;
input [7:0] DadoEscrito;
output reg [7:0] Dado1, Dado2;
output reg [7:0] SBEQ;
reg [7:0] RF [3:0];  

always begin @(posedge clock)
SBEQ <= RF[2];
RF[0]<= 8'b00000000; 
if (reset)
	begin 
	  if (EscReg)
	    begin
		    RF[RegEscrito] <= DadoEscrito;
		  end
		Dado1 = RF[RegLido1];
		Dado2 = RF[RegLido2];
	end
	
end
// 00 --> zero
// 10 --> beq

endmodule

