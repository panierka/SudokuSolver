using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.UI;

namespace Assets.Scripts.Camera
{
    public class DeviceCameraPreview : MonoBehaviour
    {
        [SerializeField]
        private RawImage image;

        [SerializeField]
        private AspectRatioFitter fitter;

        private WebCamTexture webCamTexture;

        public void BindWebCameraTexture(WebCamTexture webCamTexture)
        {
            this.webCamTexture = webCamTexture;
            image.texture = webCamTexture;
        }

        private void Update()
        {
            if (webCamTexture == null)
            {
                return;
            }

            var ratio = (float)webCamTexture.height / webCamTexture.width;
            fitter.aspectRatio = ratio;

            var a = -webCamTexture.videoRotationAngle;
            image.rectTransform.localEulerAngles = new Vector3(0, 0, a);
        }
    }
}
