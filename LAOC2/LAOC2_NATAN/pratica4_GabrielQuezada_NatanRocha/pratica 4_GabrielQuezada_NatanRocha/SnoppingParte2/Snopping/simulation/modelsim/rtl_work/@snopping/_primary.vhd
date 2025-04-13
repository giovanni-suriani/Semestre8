library verilog;
use verilog.vl_types.all;
entity Snopping is
    port(
        i_Clock         : in     vl_logic;
        i_Start         : in     vl_logic;
        i_Instruction   : in     vl_logic_vector(12 downto 0)
    );
end Snopping;
