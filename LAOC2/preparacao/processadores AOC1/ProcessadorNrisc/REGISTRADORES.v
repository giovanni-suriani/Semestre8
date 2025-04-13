module REGISTRADORES (
  input wire clk,
  input wire [3:2] readRegister1,
  input wire [1:0] readRegister2,
  input wire [2:0] writeRegister,
  input wire [7:0] writeData,
  input wire writeEnable,
  output reg [7:0] readData1,
  output reg [7:0] readData2
);

  reg [7:0] registers [0:7];

  always @(posedge clk) begin
    if (writeEnable)
      registers[writeRegister] <= writeData;
  end

  always @(negedge) begin
    readData1 = registers[readRegister1];
    readData2 = registers[readRegister2];
  end

endmodule

module REGISTRADORESteste;
	reg clk;
	reg [3:2] readRegister1;
   reg [1:0] readRegister2;
   reg [2:0] writeRegister;
   reg [7:0] writeData;
   reg writeEnable;
   wire [7:0] readData1;
   wire [7:0] readData2;
 
	REGISTRADORES REGISTRADORES (readRegister1, readRegister2, writeRegister, writeData, writeEnable);
	
	  initial begin
    clock = 0;
    readRegister1 = 0;
    readRegister2 = 0;
    writeRegister = 0;
    writeData = 0;
    writeEnable = 0;

    $display("Teste: Escrevendo em $t0");
    $display("Ao supor que existe o valor 4 armazenado na memória");
    REGISTRADORES.readData1[1] = 4;
    $display(
        "Ao supor também que o valor 1 na entrada writeData do banco de registradores");
    $display("o Valor de $t0 antes da mudança: %d", REGISTRADORES.readData1[2]);
    readReg1  = 4;
    readReg2  = 1;
    writeReg  = 4;
    writeData = 8'b00000010;
    writeEnable  = 1;
    #1 clock = 1;
    #1 clock = 0;
    $display("O valor de $t0 depois da mudança: %d", REGISTRADORES.readData1[2]);
	 end
	
	
	
	
endmodule