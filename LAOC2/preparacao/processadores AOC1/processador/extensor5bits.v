module extensor5bits(entrada,saida);
input [4:0]entrada;
output [7:0] saida;

assign saida = {3'b000,entrada[4:0]};

endmodule

