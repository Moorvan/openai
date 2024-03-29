from chat_client import *

message = [
    system(
        "You are an expert in the field of hardware model detection. You are proficient in generating corresponding vmt model descriptions based on Chisel and Verilog languages. vmt is an extension of smt language that uses annotations to define the initial state, transition formulas, and properties of the migration model. The following material is an official introduction to the vmt language: Verification Modulo Theories was originally proposed in the Rich-Model Toolkit meeting held in Turin in 2011 (see slides below). Since then, a format has been defined (see below), and is now supported by the the nuXmv model checker. The VMT format is an extension of the SMT-LIBv2 (SMT2 for short) format to represent symbolic transition systems. VMT exploits the capability offered by the SMT2 language of attaching annotations to terms and formulas in order to specify the components of the transition system and the properties to verify. Core language In the core VMT-LIB language, the following annotations are used: :next name is used to represent state variables. For each variable x in the model, the VMT file contains a pair of variables, xc and xn, representing respectively the current and next version of x. The two variables are linked by annotating xc with the attribute :next xn. All the variables that are not in relation with another by means of a :next attribute are considered inputs. :init is used to specify the formula for the initial states of the model. This formula should contain neither next-state variables nor input variables. :trans is used to specify the formula for the transition relation. :invar-property idx is used to specify invariant properties, i.e. formulas of the form Gp, where p is the formula annotated with :invar-property. The non-negative integer idx is a unique identifier for the property. :live-property idx is used to specify an LTL property of the form F Gp, where p is the formula annotated with :live-property. The non-negative integer idx is a unique identifier for the property. In a VMT file, only annotated terms and their sub-terms are meaningful. Any other term is ignored. Moreover, only the following commands are allowed to occur in VMT files: set-logic, set-option, declare-sort, define-sort, declare-fun, define-fun (For convenience, an additional (assert true) command is allowed to appear at the end of the file). The following example shows a simple NUXMV model and its corresponding VMT translation. nuXmv -- this is a comment MODULE main VAR x : integer; IVAR b : boolean; INIT x = 1; TRANS next(x) = b ? x + 1 : x; INVARSPEC x > 0; LTLSPEC FG x > 10; VMT ; this is a comment (declare-const x Int) (declare-const x.next Int) (define-fun sv.x () Int (! x :next x.next)) (declare-const b Bool) (define-fun init () Bool (! (= x 1) :init true)) (define-fun trans () Bool (! (= x.next (ite b (+ x 1) x)) :trans true) (define-fun p1 () Bool (! (> x 0) :invar-property 1)) (define-fun p2 () Bool (! (> x 10) :live-property 2)) Since the SMT2 format (and thus also the VMT one that inherits from SMT2) does not allow to annnotate the declaration of variables, it is a good practice to insert immediately after the declaration of the variables a set of defines to specify the relations among variables. See for instance the define sv0 in the example above that introduces the relation between x and xn."),
    user(
        "Starting now, I will input: 1. Hardware modules defined by Chisel; 2. Hardware definition in SystemVerilog compiled by Chisel; 3. SMT description obtained by using Yosys to convert SystemVerilog. In the obtained SMT description, the variable names have been distorted, resulting in poor readability. Now, you need to implement: 1. Replace the variable names in the generated SMT with more readable ones; 2. Remove redundant parts in the SMT and simplify it as much as possible; 3. Add comments to each line; 4. Generate the corresponding VMT, ensuring a well-described state variable and transition relationships. Tips: 1. in Transition System, you can remove clock signal in SystemVerilog"),
    assistant(
        "OK, I will start working on it. Please tell me hardware modules defined by Chisel, hardware definition in SystemVerilog compiled by Chisel, and SMT description obtained by using Yosys to convert SystemVerilog."),
    user("""
SystemVerilog:
module Memory(
  input        clock,
  input  [7:0] read_addr,
  input  [7:0] write_addr,
  input  [7:0] data_in,
  output [7:0] data_out
);
  reg [0:7] mem[0:255];
  assign data_out = mem[read_addr];
  always @(posedge clock) begin
    mem[write_addr] <= data_in;
  end
endmodule
SMT:
; SMT-LIBv2 description generated by Yosys 0.23+1 (git sha1 faa1c2e7f, aarch64-apple-darwin20.2-clang 10.0.0-4ubuntu1 -fPIC -Os)
; yosys-smt2-module Memory
(declare-sort |Memory_s| 0)
(declare-fun |Memory_is| (|Memory_s|) Bool)
(declare-fun |Memory#0| (|Memory_s|) Bool) ; \clock
; yosys-smt2-input clock 1
; yosys-smt2-clock clock posedge
; yosys-smt2-witness {"offset": 0, "path": ["\\clock"], "smtname": "clock", "smtoffset": 0, "type": "posedge", "width": 1}
; yosys-smt2-witness {"offset": 0, "path": ["\\clock"], "smtname": "clock", "smtoffset": 0, "type": "input", "width": 1}
(define-fun |Memory_n clock| ((state |Memory_s|)) Bool (|Memory#0| state))
(declare-fun |Memory#1| (|Memory_s|) (_ BitVec 8)) ; \data_in
; yosys-smt2-input data_in 8
; yosys-smt2-witness {"offset": 0, "path": ["\\data_in"], "smtname": "data_in", "smtoffset": 0, "type": "input", "width": 8}
(define-fun |Memory_n data_in| ((state |Memory_s|)) (_ BitVec 8) (|Memory#1| state))
; yosys-smt2-memory mem 8 8 1 1 sync
; yosys-smt2-witness {"path": ["\\mem"], "rom": false, "size": 256, "smtname": "mem", "statebv": false, "type": "mem", "uninitialized": [{"offset": 0, "width": 2048}], "width": 8}
(declare-fun |Memory#2#0| (|Memory_s|) (Array (_ BitVec 8) (_ BitVec 8))) ; mem
(define-fun |Memory_m mem| ((state |Memory_s|)) (Array (_ BitVec 8) (_ BitVec 8)) (|Memory#2#0| state))
(declare-fun |Memory#3| (|Memory_s|) (_ BitVec 8)) ; \read_addr
(define-fun |Memory_m:R0A mem| ((state |Memory_s|)) (_ BitVec 8) (|Memory#3| state)) ; \read_addr
(define-fun |Memory#4| ((state |Memory_s|)) (_ BitVec 8) (select (|Memory#2#0| state) (|Memory_m:R0A mem| state))) ; \data_out
(define-fun |Memory_m:R0D mem| ((state |Memory_s|)) (_ BitVec 8) (|Memory#4| state))
; yosys-smt2-output data_out 8
(define-fun |Memory_n data_out| ((state |Memory_s|)) (_ BitVec 8) (|Memory#4| state))
; yosys-smt2-input read_addr 8
; yosys-smt2-witness {"offset": 0, "path": ["\\read_addr"], "smtname": "read_addr", "smtoffset": 0, "type": "input", "width": 8}
(define-fun |Memory_n read_addr| ((state |Memory_s|)) (_ BitVec 8) (|Memory#3| state))
(declare-fun |Memory#5| (|Memory_s|) (_ BitVec 8)) ; \write_addr
; yosys-smt2-input write_addr 8
; yosys-smt2-witness {"offset": 0, "path": ["\\write_addr"], "smtname": "write_addr", "smtoffset": 0, "type": "input", "width": 8}
(define-fun |Memory_n write_addr| ((state |Memory_s|)) (_ BitVec 8) (|Memory#5| state))
(define-fun |Memory_m:W0A mem| ((state |Memory_s|)) (_ BitVec 8) (|Memory#5| state)) ; \write_addr
(define-fun |Memory_m:W0D mem| ((state |Memory_s|)) (_ BitVec 8) (|Memory#1| state)) ; \data_in
(define-fun |Memory_m:W0M mem| ((state |Memory_s|)) (_ BitVec 8) #b11111111) ; 8'11111111
(define-fun |Memory#2#1| ((state |Memory_s|)) (Array (_ BitVec 8) (_ BitVec 8)) (ite (= (|Memory_m:W0M mem| state) #b00000000) (|Memory#2#0| state) (store (|Memory#2#0| state) (|Memory_m:W0A mem| state) (bvor (bvand (|Memory_m:W0D mem| state) (|Memory_m:W0M mem| state)) (bvand (select (|Memory#2#0| state) (|Memory_m:W0A mem| state)) (bvnot (|Memory_m:W0M mem| state))))))) ; mem
(define-fun |Memory_a| ((state |Memory_s|)) Bool true)
(define-fun |Memory_u| ((state |Memory_s|)) Bool true)
(define-fun |Memory_i| ((state |Memory_s|)) Bool true)
(define-fun |Memory_h| ((state |Memory_s|)) Bool true)
(define-fun |Memory_t| ((state |Memory_s|) (next_state |Memory_s|)) Bool 
  (= (|Memory#2#1| state) (|Memory#2#0| next_state)) ; mem
) ; end of module Memory
; yosys-smt2-topmod Memory
; end of yosys output
        """),
    assistant("""
VMT:
(declare-const data_in (_ BitVec 8)) ; data_in:  8'0..8'255
(declare-const data_in.next (_ BitVec 8)) ; data_in:  8'0..8'255
(define-fun sv.data_in () (_ BitVec 8) (!
  data_in
:next data_in.next
))

(declare-const mem (Array (_ BitVec 8) (_ BitVec 8))); mem: [8'0..8'255][8'0..8'255]
(declare-const mem.next (Array (_ BitVec 8) (_ BitVec 8))); mem: [8'0..8'255][8'0..8'255]
(define-fun sv.mem () (Array (_ BitVec 8) (_ BitVec 8)) (!
  mem
  :next mem.next
))

(declare-const read_addr (_ BitVec 8)) ; read_addr: state -> 8'0..8'255
(declare-const read_addr.next (_ BitVec 8)) ; read_addr: state -> 8'0..8'255
(define-fun sv.read_addr () (_ BitVec 8) (!
  read_addr
  :next read_addr.next
))

(define-fun get_read_addr () (_ BitVec 8) (read_addr))


(define-fun data_out () (_ BitVec 8) (select mem get_read_addr)) ; data_out(state) = mem(state)[read_addr(state)]

(declare-const write_addr (_ BitVec 8)) ; write_addr: state -> 8'0..8'255
(declare-const write_addr.next (_ BitVec 8)) ; write_addr: state -> 8'0..8'255
(define-fun sv.write_addr () (_ BitVec 8) (!
  write_addr
  :next write_addr.next
))

(define-fun get_write_addr () (_ BitVec 8) (write_addr)) ; get_write_addr(state) = write_addr(state)

(define-fun get_data_in () (_ BitVec 8) (data_in)) ; get_data_in(state) = data_in(state)

(define-fun const_1 () (_ BitVec 8) (#b11111111)) ; const_1(state) = 8'255

(define-fun update_mem () (Array (_ BitVec 8) (_ BitVec 8))
  (ite (= (const_1) #b00000000)
    (mem)
    (store (mem) (get_write_addr state)
      (bvor
        (bvand (get_data_in) (const_1))
        (bvand
          (select (mem) (get_write_addr))
          (bvnot (const_1))
        ) ; 0
      ) ; data_in
    )
  )
) ; update_mem(state) = ite(const_1(state) = 8'0, mem(state), store(mem(state), get_write_addr(state), (get_data_in(state) & const_1(state)) | (mem(state)[get_write_addr(state)] & ~const_1(state))))

; Transition System

(define-fun init () Bool (!
  (forall ((addr (_ BitVec 8)))
    (= (select mem addr) #b00000000)
  ) :init true
)) ; init

(define-fun trans () Bool (!
  (= mem.next (update_mem))
  :trans true
)) ; trans() = (mem(state0.next) = update_mem(state0))
        """)
]

memory_rtl = """
A new case:
Chisel: 
class Memory(c: Int, w: Int) extends Module with Formal {
  val nw = log2Ceil(c)
  val io = IO(new Bundle {
    val wrEna = Input(Bool())
    val wrData = Input(UInt(w.W))
    val wrAddr = Input(UInt(nw.W))
    val rdAddr = Input(UInt(nw.W))
    val rdData = Output(UInt(w.W))
  })
  val mem = Mem(c, UInt(w.W))
  val a = true.B

  when(io.wrEna) {
    mem.write(io.wrAddr, io.wrData)
  }

  io.rdData := mem.read(io.rdAddr)
}
SystemVerilog:
module Memory(
  input        clock,
  input        reset,
  input        io_wrEna,
  input  [7:0] io_wrData,
  input  [4:0] io_wrAddr,
  input  [4:0] io_rdAddr,
  output [7:0] io_rdData
);
`ifdef RANDOMIZE_MEM_INIT
  reg [31:0] _RAND_0;
`endif // RANDOMIZE_MEM_INIT
  reg [7:0] mem [0:31]; // @[Memory.scala 16:16]
  wire  mem_io_rdData_MPORT_en; // @[Memory.scala 16:16]
  wire [4:0] mem_io_rdData_MPORT_addr; // @[Memory.scala 16:16]
  wire [7:0] mem_io_rdData_MPORT_data; // @[Memory.scala 16:16]
  wire [7:0] mem_MPORT_data; // @[Memory.scala 16:16]
  wire [4:0] mem_MPORT_addr; // @[Memory.scala 16:16]
  wire  mem_MPORT_mask; // @[Memory.scala 16:16]
  wire  mem_MPORT_en; // @[Memory.scala 16:16]
  assign mem_io_rdData_MPORT_en = 1'h1;
  assign mem_io_rdData_MPORT_addr = io_rdAddr;
  assign mem_io_rdData_MPORT_data = mem[mem_io_rdData_MPORT_addr]; // @[Memory.scala 16:16]
  assign mem_MPORT_data = io_wrData;
  assign mem_MPORT_addr = io_wrAddr;
  assign mem_MPORT_mask = 1'h1;
  assign mem_MPORT_en = io_wrEna;
  assign io_rdData = mem_io_rdData_MPORT_data; // @[Memory.scala 23:13]
  always @(posedge clock) begin
    if (mem_MPORT_en & mem_MPORT_mask) begin
      mem[mem_MPORT_addr] <= mem_MPORT_data; // @[Memory.scala 16:16]
    end
  end
// Register and memory initialization
`ifdef RANDOMIZE_GARBAGE_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_INVALID_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_REG_INIT
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_MEM_INIT
`define RANDOMIZE
`endif
`ifndef RANDOM
`define RANDOM $random
`endif
`ifdef RANDOMIZE_MEM_INIT
  integer initvar;
`endif
`ifndef SYNTHESIS
`ifdef FIRRTL_BEFORE_INITIAL
`FIRRTL_BEFORE_INITIAL
`endif
initial begin
  `ifdef RANDOMIZE
    `ifdef INIT_RANDOM
      `INIT_RANDOM
    `endif
    `ifndef VERILATOR
      `ifdef RANDOMIZE_DELAY
        #`RANDOMIZE_DELAY begin end
      `else
        #0.002 begin end
      `endif
    `endif
`ifdef RANDOMIZE_MEM_INIT
  _RAND_0 = {1{`RANDOM}};
  for (initvar = 0; initvar < 32; initvar = initvar+1)
    mem[initvar] = _RAND_0[7:0];
`endif // RANDOMIZE_MEM_INIT
  `endif // RANDOMIZE
end // initial
`ifdef FIRRTL_AFTER_INITIAL
`FIRRTL_AFTER_INITIAL
`endif
`endif // SYNTHESIS
endmodule
"""

counter_rtl = """
I have a new case: Chisel:
class Counter(max: Int) extends Module {
  val io = IO(new Bundle {
    val out = Output(UInt(log2Ceil(max).W))
  })
  val count = RegInit(0.U(log2Ceil(max).W))
  count := count + 1.U
  io.out := count
}
SystemVerilog:
module Counter(
  input        clock,
  input        reset,
  output [3:0] io_out
);
`ifdef RANDOMIZE_REG_INIT
  reg [31:0] _RAND_0;
`endif // RANDOMIZE_REG_INIT
  reg [3:0] count; // @[A.scala 11:22]
  wire [3:0] _count_T_1 = count + 4'h1; // @[A.scala 12:18]
  assign io_out = count; // @[A.scala 13:10]
  always @(posedge clock) begin
    if (reset) begin // @[A.scala 11:22]
      count <= 4'h0; // @[A.scala 11:22]
    end else begin
      count <= _count_T_1; // @[A.scala 12:9]
    end
  end
// Register and memory initialization
`ifdef RANDOMIZE_GARBAGE_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_INVALID_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_REG_INIT
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_MEM_INIT
`define RANDOMIZE
`endif
`ifndef RANDOM
`define RANDOM $random
`endif
`ifdef RANDOMIZE_MEM_INIT
  integer initvar;
`endif
`ifndef SYNTHESIS
`ifdef FIRRTL_BEFORE_INITIAL
`FIRRTL_BEFORE_INITIAL
`endif
initial begin
  `ifdef RANDOMIZE
    `ifdef INIT_RANDOM
      `INIT_RANDOM
    `endif
    `ifndef VERILATOR
      `ifdef RANDOMIZE_DELAY
        #`RANDOMIZE_DELAY begin end
      `else
        #0.002 begin end
      `endif
    `endif
`ifdef RANDOMIZE_REG_INIT
  _RAND_0 = {1{`RANDOM}};
  count = _RAND_0[3:0];
`endif // RANDOMIZE_REG_INIT
  `endif // RANDOMIZE
end // initial
`ifdef FIRRTL_AFTER_INITIAL
`FIRRTL_AFTER_INITIAL
`endif
`endif // SYNTHESIS
endmodule
    """


def getVMT(source: str):
    return chat_to_gpt(model_4, message, text=source)


if __name__ == '__main__':
    set_debug()
    print(getVMT(counter_rtl))
