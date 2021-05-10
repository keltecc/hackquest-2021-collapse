using System;

namespace ZN.Runner
{
    internal static class CycleStringReader
    {
        private static int index;
        private static string[] parts;

        public static void Refresh()
        {
            index = 0;
        }

        public static void SetString(string str)
        {
            parts = str.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            Refresh();
        }

        public static void ClearString()
        {
            index = -1;
            parts = new string[0];
        }

        public static bool TryRead<T>(out T value)
        {
            value = default(T);

            if (!TryReadNextPart(out var part))
            {
                return false;
            }

            value = (T)Convert.ChangeType(part, typeof(T));
            return true;
        }

        private static bool TryReadNextPart(out string part)
        {
            part = null;

            if (index >= parts.Length)
            {
                return false;
            }

            part = parts[index];
            index += 1;
            return true;
        }
    }
}
