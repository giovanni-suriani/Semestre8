 module clock(CLK);
 output reg CLK;
 
 initial 
 CLK = 0;
 
 always 
 #1 CLK = ~CLK;
 
 endmodule