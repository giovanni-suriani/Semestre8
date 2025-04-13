module Receptor (
    input wire [1:0] i_Message
);
  // States
  localparam [1:0] INVALID = 0;
  localparam [1:0] SHARED = 1;
  localparam [1:0] MODIFIED = 2;
  reg [1:0] r_State;

  // Actions
  localparam [1:0] WRITEBACK = 1;
  localparam [1:0] ABORT = 2;
  localparam [1:0] WRITEBACK_AND_ABORT = 3;
  reg [1:0] r_Signal = 0;

  // Messages
  localparam [1:0] READ_MISS = 1;
  localparam [1:0] WRITE_MISS = 2;
  localparam [1:0] INVALIDATE = 3;

  initial r_State <= SHARED;

  always @(i_Message) begin
    case (r_State)
      INVALID: begin
        r_Signal <= 0;
        r_State  <= INVALID;
      end
      MODIFIED: begin
        case (i_Message)
          READ_MISS: begin
            r_Signal <= WRITEBACK_AND_ABORT;
            r_State  <= SHARED;
          end
          WRITE_MISS: begin
            r_Signal <= WRITEBACK_AND_ABORT;
            r_State  <= INVALID;
          end
        endcase
      end
      SHARED: begin
        case (i_Message)
          READ_MISS: begin
            r_Signal <= 0;
            r_State  <= SHARED;
          end
          WRITE_MISS, INVALIDATE: begin
            r_Signal <= 0;
            r_State  <= INVALID;
          end
        endcase
      end
    endcase
  end

endmodule
