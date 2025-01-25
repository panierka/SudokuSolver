using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UnityEngine.Networking;
using UnityEngine;

namespace Assets.Scripts.Api
{
    public class FileUploader
    {
        public IEnumerator SendFileToServer<TResponse>(byte[] rawData, string url, Callback<TResponse> callback, Callback<string> fallback)
        {
            var request = new UnityWebRequest(url, UnityWebRequest.kHttpVerbPOST);
            var uploadHandler = new UploadHandlerRaw(rawData)
            {
                contentType = "application/octet-stream"
            };

            request.uploadHandler = uploadHandler;
            request.downloadHandler = new DownloadHandlerBuffer();

            request.SetRequestHeader("Content-Type", "application/octet-stream");

            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                var responseText = request.downloadHandler.text;

                Debug.Log($"response: {responseText}");

                var responseObject = JsonUtility.FromJson<TResponse>(responseText);
                callback(responseObject);
            }
            else
            {
                fallback(request.error);
            }
        }
    }
}
