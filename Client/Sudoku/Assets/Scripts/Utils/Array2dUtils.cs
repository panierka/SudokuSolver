using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Assets.Scripts.Utils
{
    public static class Array2dUtils
    {
        public static int[,] FromList(List<List<int>> list)
        {
            var maxX = list.Count;
            var maxY = list.First().Count;

            var matrix = new int[maxX, maxY];

            for (int y = 0; y < maxY; y++)
            {
                for (int x = 0; x < maxX; x++)
                {
                    matrix[x, y] = list[y][x];
                }
            }

            return matrix;
        }
    }
}
