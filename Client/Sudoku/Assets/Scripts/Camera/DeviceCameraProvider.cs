using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Assets.Scripts.Camera
{
    public class DeviceCameraProvider : MonoBehaviour
    {
        [SerializeField]
        private UnityEvent<WebCamTexture> onBackCameraInitialized;

        public WebCamTexture BackCamera { get; private set; }

        private void Awake()
        {
            var cameraDevices = WebCamTexture.devices;
            var backCameraDevices = cameraDevices
                .Where(x => !x.isFrontFacing);

            if (!backCameraDevices.Any())
            {
                Debug.LogError("No camera device");
                return;
            }

            var device = backCameraDevices.First();
            BackCamera = new WebCamTexture(device.name, Screen.width, Screen.height);
            BackCamera.Play();

            onBackCameraInitialized?.Invoke(BackCamera);    
        }
    }
}
