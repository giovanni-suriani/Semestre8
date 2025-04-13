module Cache #(
    parameter IDENTIFIER = 0,
    parameter DATA_FILE  = 0
) (
    input wire i_Clock,
    input wire i_Start,
    input wire [12:0] i_Instruction,
    input wire [23:0] i_Bus,
    output reg [23:0] o_Bus
);

  localparam [1:0] INVALID = 0;
  localparam [1:0] SHARED = 1;
  localparam [1:0] MODIFIED = 2;

  localparam [1:0] RM = 0;
  localparam [1:0] WM = 1;
  localparam [1:0] INV = 2;

  /*
    Tags:
    100 -> 0 = 0 % 4 = 0
    108 -> 1 = 1 % 4 = 1
    110 -> 2 = 2 % 4 = 2
    118 -> 3 = 3 % 4 = 3
    120 -> 4 = 0 % 4 = 0
    128 -> 5 = 1 % 4 = 1
    130 -> 6 = 2 % 4 = 2  
  */

  /*
    [11:10] => State
    [9:7] => TAG
    [6:0] => DATA
  */
  reg [11:0] r_Memory[0:3];
  initial $readmemb(DATA_FILE, r_Memory);

  /*
    [12] => 0: Read, 1: Write
    [11:10] => 00: PO, 01: P1, 11: P3
    [9:7] => TAG
    [6:0] => DATA
  */
  wire w_InsOp = i_Instruction[12];
  wire w_InsPo = i_Instruction[11:10] == IDENTIFIER;
  wire [2:0] w_InsTag = i_Instruction[9:7];
  wire [6:0] w_InsData = i_Instruction[6:0];

  wire [1:0] w_MemIndex = w_InsTag % 4;
  wire [1:0] w_MemState = r_Memory[w_MemIndex][11:10];
  wire [2:0] w_MemTag = r_Memory[w_MemIndex][9:7];
  wire [6:0] w_MemData = r_Memory[w_MemIndex][6:0];

  localparam STEP0 = 0;
  localparam STEP1 = 1;
  localparam STEP2 = 2;
  localparam STEP3 = 3;
  reg [3:0] r_Step = STEP0;

  reg r_WaitingValue = 0;
  reg r_FromP = 0;
  always @(posedge i_Clock) begin
    o_Bus = 0;

    case (r_Step)
      STEP0: begin
        if (i_Start) begin
          r_Step  = STEP1;
          r_FromP = 0;
        end
      end

      STEP1: begin
        r_WaitingValue = 0;

        if (w_InsPo) begin  // A instrução é para esse processador

          // Verifica tipo da instrução
          if (w_InsOp) begin
            // A instrução é de escrita

            if (w_MemState == INVALID) begin
              // Place write miss on bus
              r_Memory[w_MemIndex] = {MODIFIED, w_InsTag, w_InsData};
              o_Bus = {1'b0, WM, w_InsTag, w_InsData, 1'b0, w_MemTag, w_MemData};
            end else if (w_MemState == SHARED) begin

              if (w_MemTag == w_InsTag) begin
                // CPU write hit / invalidate on bus
                r_Memory[w_MemIndex] = {MODIFIED, w_InsTag, w_InsData};
                o_Bus = {1'b0, INV, w_InsTag, w_InsData, 1'b0, w_MemTag, w_MemData};
              end else begin
                // Place write miss on bus
                r_Memory[w_MemIndex] = {MODIFIED, w_InsTag, w_InsData};
                o_Bus = {1'b0, WM, w_InsTag, w_InsData, 1'b0, w_MemTag, w_MemData};
              end

            end else begin

              if (w_MemTag == w_InsTag) begin
                // CPU write hit
                r_Memory[w_MemIndex] = {MODIFIED, w_InsTag, w_InsData};
              end else begin
                // Place write miss on bus / write back
                o_Bus = {1'b0, WM, w_InsTag, w_InsData, 1'b1, w_MemTag, w_MemData};
                r_Memory[w_MemIndex] = {MODIFIED, w_InsTag, w_InsData};
              end

            end

          end else begin

            // A instrução é de leitura    
            if (w_MemState == INVALID) begin
              // Place read miss on bus
              r_Memory[w_MemIndex] = {SHARED, w_InsTag, 7'b0};
              o_Bus = {1'b0, RM, w_InsTag, w_InsData, 1'b0, w_MemTag, w_MemData};
              r_WaitingValue = 1;
            end else if (w_MemState == SHARED) begin

              if (w_MemTag == w_InsTag) begin
                // CPU read hit
              end else begin
                // Place read miss on bus
                r_Memory[w_MemIndex] = {SHARED, w_InsTag, 7'b0};
                o_Bus = {1'b0, RM, w_InsTag, 7'b0, 1'b0, w_MemTag, w_MemData};
                r_WaitingValue = 1;
              end

            end else begin

              if (w_MemTag == w_InsTag) begin
                // CPU read hit
              end else begin
                // Place read miss on bus / write back
                o_Bus = {1'b0, RM, w_InsTag, 7'b0, 1'b1, w_MemTag, w_MemData};
                r_Memory[w_MemIndex] = {SHARED, w_InsTag, 7'b0};
                r_WaitingValue = 1;
              end
            end
          end
        end

        r_Step = STEP2;
      end

      STEP2: begin
        r_Step = STEP3;
      end

      STEP3: begin
        if (r_WaitingValue) begin
          $display("Recebido %b %2d", r_FromP, i_Bus[17:11]);
          if (i_Bus[23]) r_Memory[w_MemIndex][6:0] = i_Bus[17:11];
          else r_Memory[w_MemIndex][6:0] = i_Bus[6:0];
        end

        r_Step = STEP0;
      end
    endcase

  end

  /*
    [22-21] => 0 -> RM, 1 -> WM, 2   -> Invalidate
    [20-18] => TAG
    [17-11] => DATA
    [10] => WB?
    [9-7] => TAG
    [6-0] => DATA
  */
  integer receptorIndex = 0;
  always @(i_Bus) begin
    receptorIndex = 0;

    if (!w_InsPo) begin  // A instrução não é para esse processador

      receptorIndex = i_Bus[20:18] % 4;
      if (i_Bus[20:18] == r_Memory[receptorIndex][9:7]) begin
        if (r_Memory[receptorIndex][11:10] == INVALID) begin
          // Não faz nada
        end else if (r_Memory[receptorIndex][11:10] == SHARED) begin
          if (i_Bus[22:21] == INV || i_Bus[22:21] == WM) begin

            //Invalidate and Write Miss
            r_Memory[receptorIndex][11:10] = INVALID;
          end

        end else begin
          // Check Write Miss and Read Miss

          if (i_Bus[22:21] == WM) begin
            // Writeback block / Abort Memoru Access
            o_Bus = {
              1'b1,
              WM,
              r_Memory[receptorIndex][9:7],
              r_Memory[receptorIndex][6:0],
              1'b1,
              r_Memory[receptorIndex][9:7],
              r_Memory[receptorIndex][6:0]
            };
            r_Memory[receptorIndex][11:10] = INVALID;
          end

          if (i_Bus[22:21] == RM) begin
            // Writeback block / Abort Memoru Access
            r_FromP = 1;
            o_Bus = {
              1'b1,
              WM,
              r_Memory[receptorIndex][9:7],
              r_Memory[receptorIndex][6:0],
              1'b1,
              r_Memory[receptorIndex][9:7],
              r_Memory[receptorIndex][6:0]
            };
            r_Memory[receptorIndex][11:10] = SHARED;
          end
        end

      end

    end
  end

endmodule
