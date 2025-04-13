module Emissor (
    input wire i_Clock,
    input wire i_Start,
    input wire [1:0] i_Operation,

    output wire [1:0] o_Message
);
  // States
  localparam [1:0] INVALID = 0;
  localparam [1:0] SHARED = 1;
  localparam [1:0] MODIFIED = 2;
  reg [1:0] r_State;

  // Messages
  localparam [1:0] READ_MISS = 1;
  localparam [1:0] WRITE_MISS = 2;
  localparam [1:0] INVALIDATE = 3;
  reg [1:0] r_Message = 0;

  // Actions
  localparam [1:0] WRITEBACK = 1;
  localparam [1:0] ABORT = 2;
  reg [1:0] r_Action = 0;

  // Operations
  localparam [1:0] RM = 0;
  localparam [1:0] RH = 1;
  localparam [1:0] WM = 2;
  localparam [1:0] WH = 3;

  initial r_State <= INVALID;

  localparam STEP0 = 0;
  localparam STEP1 = 1;
  reg [1:0] r_Step = STEP0;

  always @(posedge i_Clock) begin

    case (r_Step)
      STEP0: begin
        if (i_Start) begin
          r_Step <= STEP1;
        end
      end
      STEP1: begin
        case (r_State)
          INVALID: begin
            case (i_Operation)
              RM, RH: begin
                r_Message <= READ_MISS;
                r_Action  <= 0;
                r_State   <= SHARED;
              end
              WM, WH: begin
                r_Message <= WRITE_MISS;
                r_Action  <= 0;
                r_State   <= MODIFIED;
              end
            endcase
          end
          MODIFIED: begin
            case (i_Operation)
              WH, RH: begin
                r_Message <= 0;
                r_Action  <= 0;
                r_State   <= MODIFIED;
              end
              WM: begin
                r_Message <= WRITE_MISS;
                r_Action  <= WRITEBACK;
                r_State   <= MODIFIED;
              end
              RM: begin
                r_Message <= READ_MISS;
                r_Action  <= WRITEBACK;
                r_State   <= SHARED;
              end
            endcase
          end
          SHARED: begin
            case (i_Operation)
              RH: begin
                r_Message <= 0;
                r_Action  <= 0;
                r_State   <= SHARED;
              end
              RM: begin
                r_Message <= READ_MISS;
                r_Action  <= 0;
                r_State   <= SHARED;
              end
              WH: begin
                r_Message <= INVALIDATE;
                r_Action  <= 0;
                r_State   <= MODIFIED;
              end
              WM: begin
                r_Message <= WRITE_MISS;
                r_Action  <= 0;
                r_State   <= MODIFIED;
              end
            endcase
          end
        endcase

        r_Step <= STEP0;
      end

    endcase


  end

  assign o_Message = r_Message;

endmodule
