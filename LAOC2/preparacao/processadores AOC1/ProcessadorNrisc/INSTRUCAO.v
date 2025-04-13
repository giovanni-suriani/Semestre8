module INSTRUCAO (
    input wire clock,
    input wire [3:0] address,
    output wire [7:0] dataOut,
);

  reg [7:0] data[30:0];

  initial begin
    data[0] = 1;
    data[1] = 15;
    data[2] = 5;
  end

  always @(negedge clock) //read/leitura na memória
    begin
      dataOut = data[address];
    end

endmodule


module INSTRUCAOteste;

  reg clock;
  reg [3:0] address;
  wire [7:0] dataOut;

  INSTRUCAO INSTRUCAO(clock, address,dataOut);

  initial begin
    clock = 0;
    address = 0;

    $display("Teste 2: Lendo da memoria");
    $display("Lendo da posicao 10 da memoria de dados");
    $display("Valor armazenado na posicao 10: %d", INSTRUCAO.data[10]);
    address = 10;
    #1 clock = 0;
    #1 clock = 1;
    $display("Valor da saida do banco de memoria: %d", dataOut);

  end

  initial begin
    $monitor("Time=%0d, Clock=%d, address=%d, dataOut=%d",
             $time, clock, address, dataOut);
  end

endmodule