from PyPDF2 import PdfReader, PdfWriter

# Load your original PDF
input_path = "VLA_28_0.secured.lect.pdf"  # Replace with your actual path
reader = PdfReader(input_path)

# Define the modules and their page ranges
modules = {
    "01_About_This_Course": (6, 12),
    "02_Describing_Verilog_Applications": (13, 29),
    "03_Verilog_Introduction": (30, 49),
    "04_Choosing_Between_Verilog_Data_Types": (50, 79),
    "05_Using_Verilog_Operators": (80, 101),
    "06_Making_Procedural_Statements": (102, 125),
    "07_Using_Blocking_and_Nonblocking_Assignments": (126, 141),
    "08_Using_Continuous_and_Procedural_Assignments": (142, 160),
    "09_Understanding_the_Simulation_Cycle": (161, 183),
    "10_Using_Functions_and_Tasks": (184, 204),
    "11_Directing_the_Compiler": (205, 218),
    "12_Introducing_the_Process_of_Synthesis": (219, 235),
    "13_Coding_RTL_for_Synthesis": (236, 263),
    "14_Designing_Finite_State_Machines": (264, 282),
    "15_Avoiding_Simulation_Mismatches": (287, 303),
    "16_Managing_the_RTL_Coding_Process": (304, 318),
    "17_Managing_the_Logic_Synthesis_Process": (319, 351),
    "18_Coding_and_Synthesizing_Example_Design": (352, 360),
    "19_Using_Verification_Constructs": (361, 383),
    "20_Coding_Design_Behavior_Algorithmically": (388, 401),
    "21_Using_System_Tasks_and_Functions": (402, 429),
    "22_Generating_Test_Stimulus": (430, 461),
    "23_Developing_a_Testbench": (462, 495),
    "24_Example_Verilog_Testbench": (496, 502),
    "25_Course_Conclusions": (503, 505),
    "26_Next_Steps": (506, 515),
    "Appendix_A_Configurations": (510, 520),
    "Appendix_B_Verilog_Primitives_and_UDPs": (521, 558),
    "Appendix_C_SDF_Annotation_Overview": (559, 581),
    "Appendix_D_SystemVerilog_and_UVM": (582, None),  # Adjust end if needed
}


# Split and write each module
for title, (start, end) in modules.items():
    writer = PdfWriter()
    for i in range(start, end + 1):
        writer.add_page(reader.pages[i])
    with open(f"{title}.pdf", "wb") as f:
        writer.write(f)
    print(f"Created: {title}.pdf")
