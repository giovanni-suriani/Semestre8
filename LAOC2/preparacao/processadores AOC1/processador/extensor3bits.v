module extensor3bits(entrada,saida);
input [2:0]entrada;
output [7:0] saida;

assign saida = {5'b00000,entrada[2:0]};

endmodule

