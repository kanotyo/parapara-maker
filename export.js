(function () {
  'use strict';

  var controls = document.querySelector('.controls');
  if (!controls || typeof window.render !== 'function') return;

  var download = document.createElement('button');
  download.id = 'download';
  download.type = 'button';
  download.textContent = 'このコマを保存';
  controls.appendChild(download);

  function updateDownload() {
    download.disabled = !window.frames.length || !window.frames[window.now];
  }

  var originalRender = window.render;
  window.render = function () {
    var result = originalRender.apply(this, arguments);
    updateDownload();
    return result;
  };

  download.addEventListener('click', function () {
    var svg = window.frames[window.now];
    if (!svg) return;

    var url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
    var link = document.createElement('a');
    link.href = url;
    link.download = 'parapara-frame-' + (window.now + 1) + '.svg';
    document.body.appendChild(link);
    link.click();
    link.remove();
    // Give the browser time to begin reading the download before revoking it.
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  });

  updateDownload();
}());
