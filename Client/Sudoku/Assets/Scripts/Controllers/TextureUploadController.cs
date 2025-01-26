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

        public void SendTexture()
        {
            var texture = textureSource.texture;
            Debug.Log(texture);

            var texture2D = Convert(texture);
            byte[] pngData = texture2D.EncodeToPNG();

            Debug.Log("sending...");
            var fu = new FileUploader();
            CoroutineHost.Instance.StartCoroutine(fu
                .SendFileToServer<SudokuSolutionModel>(
                    pngData, url, FireEvent, err => Debug.LogError(err))
            );

            onTextureSent?.Invoke(texture2D);
        }

        private void FireEvent(SudokuSolutionModel model)
        {
            Debug.Log(onSolutionReceived.GetPersistentEventCount());
            onSolutionReceived.Invoke(model);
        }

        private Texture2D Convert(Texture texture)
        {
            if (texture is Texture2D t2d)
            {             
                return t2d;
            }

            if (texture is RenderTexture renderTexture)
            {
                Texture2D texture2D = new(renderTexture.width, renderTexture.height, TextureFormat.RGBA32, false);
                RenderTexture.active = renderTexture;
                texture2D.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
                texture2D.Apply();
                return texture2D;
            }

            return null;
        }
    }
}
