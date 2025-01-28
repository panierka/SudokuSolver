using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

namespace Assets.Scripts.Utils
{
    public class CoroutineHost : MonoBehaviour
    {
        public static CoroutineHost Instance { get; private set; }

        private void Awake()
        {
            if (Instance != this)
            {
                Destroy(gameObject);
            }

            Instance = this;
            DontDestroyOnLoad(this);
        }
    }
}
