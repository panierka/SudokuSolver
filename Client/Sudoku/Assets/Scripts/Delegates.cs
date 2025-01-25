using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Assets.Scripts
{
    public delegate void Callback();
    public delegate void Callback<T>(T @object);
}
