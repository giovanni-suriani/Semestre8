library verilog;
use verilog.vl_types.all;
entity Cache is
    generic(
        IDENTIFIER      : integer := 0;
        DATA_FILE       : integer := 0
    );
    port(
        i_Clock         : in     vl_logic;
        i_Start         : in     vl_logic;
        i_Instruction   : in     vl_logic_vector(12 downto 0);
        i_Bus           : in     vl_logic_vector(23 downto 0);
        o_Bus           : out    vl_logic_vector(23 downto 0)
    );
    attribute mti_svvh_generic_type : integer;
    attribute mti_svvh_generic_type of IDENTIFIER : constant is 1;
    attribute mti_svvh_generic_type of DATA_FILE : constant is 1;
end Cache;
