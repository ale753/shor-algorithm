from braket.circuits import Circuit, circuit
from braket.devices import LocalSimulator
import math
from fractions import Fraction

def inverse_qft(qubits):
    # instantiate circuit object
    qftcirc = Circuit()
    
    # get number of qubits
    num_qubits = len(qubits)
    
    # First add SWAP gates to reverse the order of the qubits:
    for i in range(math.floor(num_qubits/2)):
        qftcirc.swap(qubits[i], qubits[-i-1])
        
    # Start on the last qubit and work to the first.
    for k in reversed(range(num_qubits)):
    
        # Apply the controlled rotations, with weights (angles) defined by the distance to the control qubit.
        # These angles are the negative of the angle used in the QFT.
        # Start on the last qubit and iterate until the qubit after k.  
        # When num_qubits==1, this loop does not run.
        for j in reversed(range(1, num_qubits - k)):
            angle = -2*math.pi/(2**(j+1))
            qftcirc.cphaseshift(qubits[k+j],qubits[k], angle)
            
        # Then add a Hadamard gate
        qftcirc.h(qubits[k])
    
    return qftcirc

#Creating the circuit for 13^i mod(35)
circuit = Circuit()

circuit.h(0)
circuit.h(1)
circuit.h(2)

circuit.ccnot(0,3,4)
circuit.cnot(0,3)

circuit.ccnot(1,3,4)
circuit.cnot(1,3)
circuit.ccnot(1,3,4)
circuit.cnot(1,3)
circuit.ccnot(1,3,4)
circuit.cnot(1,3)

circuit.ccnot(2,3,4)
circuit.cnot(2,3)
circuit.ccnot(2,3,4)
circuit.cnot(2,3)
circuit.ccnot(2,3,4)
circuit.cnot(2,3)
circuit.ccnot(2,3,4)
circuit.cnot(2,3)


circuit.add_circuit(inverse_qft(range(3)))

print(circuit)

device = LocalSimulator()

#print(device.run(circuit, shots=4).result().measurement_counts)

counts = device.run(circuit, shots=10).result().measurement_counts

for measurement in counts.keys():
    decimal = int(measurement, 2)/2**3
    print(Fraction(decimal).limit_denominator())
