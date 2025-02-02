using Assets.Scripts.Api;
using Assets.Scripts.Api.Model;
using Assets.Scripts.Utils;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Assets.Scripts.Controllers
{
    public class TextureUploadController : MonoBehaviour
    {
        [SerializeField]
        private string url;

        [SerializeField]
        private RawImage textureSource;

        [SerializeField]
        private UnityEvent<SudokuSolutionModel> onSolutionReceived;

        [SerializeField]
        private UnityEvent<Texture2D> onTextureSent;

        [SerializeField]
        private UnityEvent onError;

        public void SendTexture()
        {
            var texture = textureSource.texture;
            Debug.Log(texture);

            var converted = Convert(texture);
            var texture2D = RotateTexture(converted, true);
            byte[] pngData = texture2D.EncodeToPNG();

            Debug.Log("sending...");
            var fu = new FileUploader();
            CoroutineHost.Instance.StartCoroutine(fu
                .SendFileToServer<SudokuSolutionModel>(
                    pngData, url, FireEvent, FireErrorEvent)
            );

            onTextureSent?.Invoke(texture2D);
        }

        private void FireEvent(SudokuSolutionModel model)
        {
            Debug.Log("response received");
            onSolutionReceived.Invoke(model);
        }

        private void FireErrorEvent(string error)
        {
            Debug.LogError(error);
            onError.Invoke();
        }

        private Texture2D Convert(Texture texture)
        {
            switch (texture)
            {
                case Texture2D texture2:
                    return texture2;

                case RenderTexture renderTexture:
                    Texture2D texture2D = new(renderTexture.width, renderTexture.height, TextureFormat.RGBA32, false);
                    RenderTexture.active = renderTexture;
                    texture2D.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
                    texture2D.Apply();
                    return texture2D;

                case WebCamTexture webCamTexture:
                    Texture2D t2d = new(webCamTexture.width, webCamTexture.height, TextureFormat.RGBA32, false);
                    t2d.SetPixels32(webCamTexture.GetPixels32());
                    t2d.Apply();
                    return t2d;

                default:
                    return null;
            }
        }

		Texture2D RotateTexture(Texture2D originalTexture, bool clockwise)
		{
			Color32[] original = originalTexture.GetPixels32();
			Color32[] rotated = new Color32[original.Length];
			int w = originalTexture.width;
			int h = originalTexture.height;

			int iRotated, iOriginal;

			for (int j = 0; j < h; ++j)
			{
				for (int i = 0; i < w; ++i)
				{
					iRotated = (i + 1) * h - j - 1;
					iOriginal = clockwise ? original.Length - 1 - (j * w + i) : j * w + i;
					rotated[iRotated] = original[iOriginal];
				}
			}

			Texture2D rotatedTexture = new Texture2D(h, w);
			rotatedTexture.SetPixels32(rotated);
			rotatedTexture.Apply();
			return rotatedTexture;
		}
	}
}
