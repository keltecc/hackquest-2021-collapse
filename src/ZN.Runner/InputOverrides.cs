using System;
using Microsoft.Quantum.Simulation.Core;

using ZNUtils = ZN.Quantum.Utils;

namespace ZN.Runner
{
    internal interface InputOverride<T>
    {
        public Func<QVoid, T> __Body__ { get; }
    }

    internal class InputIntOverride : ZNUtils.InputInt, InputOverride<Int64>
    {
        public InputIntOverride(IOperationFactory m)
            : base(m)
        { }

        public override Func<QVoid, Int64> __Body__ => 
            _ => CycleStringReader.TryRead<Int64>(out var value) ? value : throw new InvalidOperationException();
    }

    internal class InputDoubleOverride : ZNUtils.InputDouble, InputOverride<Double>
    {
        public InputDoubleOverride(IOperationFactory m)
            : base(m)
        { }

        public override Func<QVoid, Double> __Body__ =>
            _ => CycleStringReader.TryRead<Double>(out var value) ? value : throw new InvalidOperationException();
    }

    internal class InputStringOverride : ZNUtils.InputString, InputOverride<String>
    {
        public InputStringOverride(IOperationFactory m)
            : base(m)
        { }

        public override Func<QVoid, String> __Body__ => _ =>
        {
            if (CycleStringReader.TryRead<String>(out var value))
            {
                return value;
            }

            CycleStringReader.Refresh();
            return String.Empty;
        };
    }
}
