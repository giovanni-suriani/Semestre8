module PC(clock, reset, enderecoE, enderecoS);
  input clock, reset;
  input [7:0] enderecoE;
  output[7:0] enderecoS;
  reg [7:0] regis;
 
  always@ (posedge clock)
  begin
    //escrita -> atualiozacao do registrador
    if(reset)
      begin
        regis = enderecoE;
      end
  end

assign enderecoS = regis;
 
endmodule
