module ULAAOC(ctrlULA,num2,num1,zero,resultado);

input ctrlULA;
input [7:0] num1,num2;
output reg zero;
output reg [7:0] resultado;

always begin @ (*)
  // zero = 1 --> salto liberado
	if(!ctrlULA) //soma
		begin
			resultado = num2 + num1;
			zero = 1'b0;
		end
	else //subtracao
		begin
			resultado = num2 - num1;
			if(resultado == 8'b00000000)
			  begin
			    zero = 1'b1;
			  end
			else
			  begin
			    zero = 1'b0;
			  end
		end
end


endmodule

