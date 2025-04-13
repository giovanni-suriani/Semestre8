module extensor2bits(entrada,saida);
input [1:0]entrada;
output [7:0] saida;

assign saida = {6'b000000,entrada[1:0]};

endmodule

