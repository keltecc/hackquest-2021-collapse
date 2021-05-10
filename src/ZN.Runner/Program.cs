using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;

using ZNQuantum = ZN.Quantum;

namespace ZN.Runner
{
    public class Program
    {
        private static async Task<byte[]> TransformBytesAsync(byte[] bytes, string input)
        {
            using var simulator = new QuantumSimulator();

            CycleStringReader.SetString(input);

            simulator.Register(typeof(ZNQuantum.Utils.InputInt), typeof(InputIntOverride));
            simulator.Register(typeof(ZNQuantum.Utils.InputDouble), typeof(InputDoubleOverride));
            simulator.Register(typeof(ZNQuantum.Utils.InputString), typeof(InputStringOverride));

            var numbers = new QArray<long>(bytes.Select(x => (long)x));
            var result = await ZNQuantum.TransformBytes.Run(simulator, numbers);

            CycleStringReader.ClearString();

            return result.Select(x => (byte)x).ToArray();
        }

        private static string BytesToString(byte[] bytes)
        {
            return BitConverter.ToString(bytes).Replace("-", "").ToLowerInvariant();
        }

        public static async Task MainAsync()
        {
            var flag = await File.ReadAllBytesAsync("flag.txt");

            while (true)
            {
                Console.Write(">>> ");
                var input = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(input))
                {
                    break;
                }

                var result = await TransformBytesAsync(flag, input);

                Console.WriteLine(BytesToString(result));
            }
        }

        public static void Main()
        {
            Task.Run(MainAsync).GetAwaiter().GetResult();
        }
    }
}
