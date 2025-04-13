module Memory (
    input wire clock,
    input wire [3:0] address,
    input wire [7:0] writeData,
    output wire [7:0] dataOut,
    input wire MemRead,
    input wire MemWrite
);

  reg [7:0] data[30:0];

  initial begin
    data[0] = 1;
    data[1] = 15;
    data[2] = 5;
  end

  always @(negedge clock) //read/leitura na memória
    begin
    if (MemRead) begin
      dataOut = data[address];
    end
  end

  always @(posedge clock) //write/escrita na memória
    begin
    if (MemWrite) begin
      data[address] = writeData;
    end
  end

endmodule


module Memoryteste;

  reg clock;
  reg [3:0] address;
  reg [7:0] writeData;
  wire [7:0] dataOut;
  reg MemRead;
  reg MemWrite;

  Memory Memory(clock, address,writeData,dataOut,MemRead,MemWrite);

  initial begin
    clock = 0;
    address = 0;
    writeData = 0;
    MemRead = 0;
    MemWrite = 0;

    $display("Teste 1: Escrevendo na memoria");
    $display("Supondo que $mem contem o valor 30");
    $display("Escrevendo no endereco 0 da memoria de dados");
    $display("Valor armazenado na posicao 0: %d", Memory.data[0]);
    MemWrite  = 1;
    writeData = 30;
    address   = 0;
    #1 clock = 1;
    #1 clock = 0;
    $display("Valor armazenado na posicao 0: %d", Memory.data[0]);
    $display("Teste 2: Lendo da memoria");
    $display("Lendo da posicao 0 da memoria de dados");
    $display("Valor armazenado na posicao 0: %d", Memory.data[0]);
    MemRead = 1;
    MemWrite = 0;
    address = 0;
    #1 clock = 0;
    #1 clock = 1;
    $display("Valor da saida do banco de memoria: %d", dataOut);

  end

  initial begin
    $monitor("Time=%0d, Clock=%d, MemRead=%b, MemWrite=%b, address=%d, writeData=%d, dataOut=%d",
             $time, clock, MemRead, MemWrite, address, writeData, dataOut);
  end

endmodule