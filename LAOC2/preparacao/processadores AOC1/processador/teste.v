module teste();
wire[7:0] SBEQ;
reg[7:0] enderecoE;
reg reset;
wire clk;
initial begin
enderecoE = 8'b00000000; reset=1;   
end

clock c2(clk);

initial begin: Init
$monitor("clk: %1b SBEQ=%8b ",clk, SBEQ);
end

processador t1(clk, enderecoE, reset, SBEQ);
  
endmodule