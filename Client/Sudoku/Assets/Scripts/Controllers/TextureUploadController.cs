using Assets.Scripts.Api;
using Assets.Scripts.Api.Model;
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
        private UnityEvent onTextureSent;

        public void SendTexture()
        {
            var texture = textureSource.texture;
            Debug.Log(texture);

            if (texture is not RenderTexture renderTexture)
            {
                return;
            }

            Texture2D texture2D = new(renderTexture.width, renderTexture.height, TextureFormat.RGBA32, false);
            RenderTexture.active = renderTexture;
            texture2D.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
            texture2D.Apply();

            byte[] pngData = texture2D.EncodeToPNG();

            Debug.Log("sending...");
            var fu = new FileUploader();
            StartCoroutine(fu
                .SendFileToServer<SudokuSolutionModel>(
                    pngData, url, FireEvent, err => Debug.LogError(err))
            );

            onTextureSent?.Invoke();
        }

        private void FireEvent(SudokuSolutionModel model)
        {
            onSolutionReceived.Invoke(model);
        }
    }
}
