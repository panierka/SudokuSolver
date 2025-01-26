using Assets.Scripts.Api.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

namespace Assets.Scripts.Utils
{
    public static class Array2dUtils
    {
        public static int[,] FromList(List<InnerList> list)
        {
            var maxX = list.Count;
            var maxY = list.First().data.Count;

            var matrix = new int[maxX, maxY];

            for (int y = 0; y < maxY; y++)
            {
                for (int x = 0; x < maxX; x++)
                {
                    matrix[x, y] = list[y].data[x];
                }
            }

            return matrix;
        }
    }
}
