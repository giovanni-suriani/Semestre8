module mux2entradas(var1, var2, sinal, saida);
input sinal;
input[1:0] var1, var2;
output reg[1:0] saida;

always @(*) begin
case(sinal)
1'b0: begin saida = var1; end
1'b1: begin saida = var2; end

endcase
end

endmodule 

