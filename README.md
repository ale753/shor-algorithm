# Shor algorithm implemented with Qiskit and AWS Bracket
In this repository you will find a quantum circuit that implements :  

<p align="center">
  <img width="100" height="50" src="https://user-images.githubusercontent.com/33957205/121774840-97553f00-cb84-11eb-9bf3-16155f949394.png">
</p>

using Qiskit and AWS Bracket both with locally simulated quantum computers. The circuit finds the prime factors of 35 with the Quantum Phase Estimation.

This exercise was proposed in the IBM Quantum Challenge 2021.

This guide will soon be available on Medium after a complete review and errors correction.

## The algorithm explained

The Shor's algorithm is composed of a classical part and a quantum part. First, a random number a between 1 and N is must be chosen, where N is the positive integer we want to find its prime factors f.

<p align="center">
  <img  width="150" height="50" src="https://user-images.githubusercontent.com/33957205/121774890-d97e8080-cb84-11eb-8750-8e7eeb779d3c.png">
</p>

The greatest common divisor of a and N is calculated. At this point, if the result is different from 1, this value is one of the prime factors and a and N are not co-prime (they have common divisors different by 1 or -1). In this case the algorithm can terminate its execution, but if the two numbers a and N are co-prime the following series of functions must be computed :

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775109-f071a280-cb85-11eb-88a7-a43dc1b77b48.png">
</p>

This periodic function will repeat itself with a certain period r . For example, given a = 3 and N = 22, the function will assume this behavior :

<p align="center">
  <img  width="460" height="300" src="https://user-images.githubusercontent.com/33957205/121775120-fc5d6480-cb85-11eb-89cd-5ebd80263ad3.png">
</p>

Where i is plotted on the x-axis. Visually, we can conclude that the period r of the function with the given values is 5. This calculation is performed by the quantum part of the algorithm with the Quantum Phase Estimation. 
At this point, to calculate the factors f the following precondition must be true :

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775132-0da67100-cb86-11eb-945e-c6a3c46c1d08.png">
</p>

In other words, r must be even. Finally, the factors are calculated with a classical algorithm (e.g. Euclid's algorithm) :

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775146-1f881400-cb86-11eb-8e21-b9f6270dd40c.png">
</p>

All these steps are summarized and formally explained in the above pseudo-code snippet.

<p align="center">
  <img  width="400" height="300" src="https://user-images.githubusercontent.com/33957205/121775160-30d12080-cb86-11eb-8bc6-6702ab9a53ca.png">
</p>

## Quantum Phase Estimation

As already mentioned, the hard part of the algorithm is finding the period r and this is achieved with the Quantum Phase Estimation. The first thing we need is a controlled version of a quantum gate U that performs the calculation of the series of functions :

<p align="center">
  <img width="170" height="50" src="https://user-images.githubusercontent.com/33957205/121775294-059b0100-cb87-11eb-9e82-48500fb498ab.png">
</p>

However, at the time of writing, it is not possible to create a circuit that performs the estimate with any value of a and N, due to error propagation of large quantum circuits that affect the outcome of the operation. There is still not a quantum machine that is scalable and capable of implement this version of the algorithm. For this reason some "a priori" informations are needed. 
The second exercise of the IBM Quantum Challenge 2021 asks to create a controlled circuit U that performs :

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775326-2b280a80-cb87-11eb-8848-e0ef87dd9b9a.png">
</p>

The series of functions with a = 13 and N = 35 is :

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775396-a2f63500-cb87-11eb-82eb-3f28a2076319.png">
</p>

<p align="center">
  <img  width="460" height="300" src="https://user-images.githubusercontent.com/33957205/121775403-b43f4180-cb87-11eb-9d4f-baad097662a7.png">
</p>

The period of the function is r = 4 and the factors are 5 and 7. To create the circuit, the four different states are encoded onto two Qbits (as suggested by the exercise).!

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775411-c7eaa800-cb87-11eb-8147-b688b7e8223d.png">
</p>

So as we can see, the circuit must be custom designed for each choice of N and a. The circuit must start with |00> and go back to |00> at the fourth iteration when the control Qbit is |1>.

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775716-94108200-cb89-11eb-80c3-b1bcdb627946.png">
</p>

The implementation of U is simple and it is done with a Toffoli gate, the quantum counterpart of the AND gate, and a CNOT gate. The toffoli gate accepts as inputs three Qbits and puts |1> on Q2 if Q0 and Q1 are |1>. The CNOT negates the second Qbit if the first one is |1>.

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775732-ac809c80-cb89-11eb-8b8a-c5f413d34b56.png">
</p>

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775723-a4286180-cb89-11eb-8a7c-32c417cf2679.png">
</p>

Q0 is the control bit, Q1 and Q2 are the input values of the gate U. The solution can be verified testing the specified input values. The python code of this specific gate is shown above.

```python
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.reset(qreg_q[0])
circuit.reset(qreg_q[1])
circuit.reset(qreg_q[2])
circuit.x(qreg_q[0])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[2], creg_c[2])
```
Three classical registers are passed to the Quantum Circuit to store the results of the measurements. The quantum registers are reset to the state |0> , the ccx (Toffoli) and cx (controlled NOT) are added to the circuit. The following figure shows that applying a not to the control qbit Q0 (so enabling the gate) will give us the result of 10 as expected with a probability of 100%.

The series of U circuits will be placed between Hadamard gates, which put the Qbits in the superposition |+>, and a block that performs the Quantum Fourier Transform of the counting registers, as shown in the following image :

<p align="center">
  <img  src="https://user-images.githubusercontent.com/33957205/121775794-fbc6cd00-cb89-11eb-96df-572846d18389.png">
</p>

Follows the implementation and simulation of the circuit, included in this repository


## References

https://en.wikipedia.org/wiki/Quantum_logic_gate

https://en.wikipedia.org/wiki/Shor%27s_algorithm

https://qiskit.org/textbook/ch-algorithms/shor.html

https://qiskit.org/textbook/ch-algorithms/quantum-phase-estimation.html

https://challenges.quantum-computing.ibm.com/iqc21

https://github.com/aws/amazon-braket-examples

https://jonathan-hui.medium.com/qc-cracking-rsa-with-shors-algorithm-bc22cb7b7767


