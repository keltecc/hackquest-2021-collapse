namespace ZN.Quantum {

    open ZN.Quantum.Utils;

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Arithmetic;

    internal function ConstructOperations (q : Qubit[]) : (Qubit => Unit is Adj + Ctl)[] {
        let size = Length(q);
        mutable ops = new (Qubit => Unit is Adj + Ctl)[0];

        repeat {
            mutable op = I;
            mutable opName = InputString();
            mutable needAdjoint = false;

            if opName == "Adjoint" {
                set needAdjoint = true;
                set opName = InputString();
            }

            if opName == "I" {
                set op = I;
            }
            // elif opName == "H" {
            //     set op = H;
            // }
            elif opName == "X" {
                set op = X;
            }
            elif opName == "Y" {
                set op = Y;
            }
            elif opName == "Z" {
                set op = Z;
            }
            elif opName == "CX" {
                let index = InputInt();

                if index >= 0 and index < size {
                    set op = CX(q[index], _);
                }
            }
            elif opName == "CY" {
                let index = InputInt();

                if index >= 0 and index < size {
                    set op = CY(q[index], _);
                }
            }
            elif opName == "CZ" {
                let index = InputInt();

                if index >= 0 and index < size {
                    set op = CZ(q[index], _);
                }
            }
            elif opName == "Rx" {
                let theta = InputDouble();
                set op = Rx(theta, _);
            }
            elif opName == "Ry" {
                let theta = InputDouble();
                set op = Ry(theta, _);
            }
            elif opName == "Rz" {
                let theta = InputDouble();
                set op = Rz(theta, _);
            }
            elif opName == "CNOT" {
                let index = InputInt();

                if index >= 0 and index < size {
                    set op = CNOT(q[index], _);
                }
            }
            elif opName == "SWAP" {
                let index = InputInt();

                if index >= 0 and index < size {
                    set op = SWAP(q[index], _);
                }
            }

            set op = needAdjoint ? Adjoint op | op;
            set ops += [op];
        }
        until opName == "";

        return ops;
    }

    internal operation ApplyOperations (q: Qubit, operations: (Qubit => Unit is Adj + Ctl)[]) : Unit {
        for op in operations {
            op(q);
        }
    }

    internal operation NumberToBigEndian (n: Int, q: Qubit[]) : Unit {
        let size = Length(q);
        mutable remainder = n;

        for i in 0 .. size - 1 {
            let qbit = q[size - 1 - i];
            Reset(qbit);

            if (remainder &&& 1) == 1 {
                X(qbit);
            }

            set remainder /= 2;
        }
    }

    internal operation BigEndianToNumber (q: Qubit[]) : Int {
        let size = Length(q);
        mutable n = 0;

        for i in 0 .. size - 1 {
            set n *= 2;
            let result = M(q[i]);

            if (IsResultOne(result)) {
                set n += 1;
            }
        }

        return n;
    }

    operation TransformBytes (ns: Int[]) : Int[] {
        let size = 8;
        let length = Length(ns);

        mutable result = new Int[length];

        for i in 0 .. length - 1 {
            let n = ns[i];

            use q = Qubit[size] {
                let carry = q[0];
                let operations = ConstructOperations(q);

                NumberToBigEndian(n, q);
                QFT(BigEndian(q));
                ApplyOperations(carry, operations);

                set result w/= i <- BigEndianToNumber(q);

                ResetAll(q);
            }
        }

        return result;
    }

}
