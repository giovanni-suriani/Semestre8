module memoDados(endereco,dadoEscrito,dadoLido,memRead,memWrite,clock,reset);
input memRead,memWrite;
input clock, reset;
input[7:0] endereco, dadoEscrito;
output reg [7:0] dadoLido;

reg [7:0] RF [7:0];

always begin @ (posedge clock)
if(reset & memWrite)
	begin
		RF[endereco] <= dadoEscrito;
	end

if(reset & memRead)
	begin
		dadoLido <= RF[endereco];
	end 

end

endmodule


