from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi
from qiskit.circuit.library import QFT
from qiskit import Aer, transpile
from qiskit.visualization import plot_histogram

from fractions import Fraction

def build_U(control, target, replication) :
    i = 0
    U_circuit = QuantumCircuit(control, target)
    for i in range (0, replication) : 
        U_circuit.ccx(0,1,2)
        U_circuit.cx(0,1)
    return U_circuit

#Creating the circuit for 13^i mod(35)

cqr = QuantumRegister(3, 'control')
tqr = QuantumRegister(2, 'target')
cux = QuantumCircuit(cqr, tqr)

cu_1 = build_U(QuantumRegister(1, 'control'), QuantumRegister(2, 'target'), 1) 
cu_2 = build_U(QuantumRegister(1, 'control'), QuantumRegister(2, 'target'), 2) 
cu_4 = build_U(QuantumRegister(1, 'control'), QuantumRegister(2, 'target'), 4) 

#Optionally convert cu_1, cu_2 and cu_4 to gates
#cu_1 = cu_1.to_gate(label="U_1")
#cu_2 = cu_2.to_gate(label="U_2")
#cu_4 = cu_4.to_gate(label="U_4")

for i in range(3):
    cux = cux.compose([cu_1, cu_2, cu_4][i], [cqr[i], tqr[0], tqr[1]])
cux.draw('mpl')

cr = ClassicalRegister(3)
shor_circuit = QuantumCircuit(cqr, tqr, cr)


shor_circuit.h(cqr)


shor_circuit = shor_circuit.compose(cux)

# Perform the inverse QFT and extract the output
shor_circuit.append(QFT(3, inverse=True), cqr)
shor_circuit.measure(cqr, cr)

print(shor_circuit)

qasm_sim = Aer.get_backend('aer_simulator')
tqc = transpile(shor_circuit, basis_gates=['u', 'cx'], optimization_level=3)
counts = qasm_sim.run(tqc).result().get_counts()
plot_histogram(counts)


for measurement in counts.keys():
    decimal = int(measurement, 2)/2**cqr.size 
    print(Fraction(decimal).limit_denominator())
