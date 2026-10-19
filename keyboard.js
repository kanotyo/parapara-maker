(function () {
  'use strict';

  var back = document.querySelector('#back');
  var next = document.querySelector('#next');
  var play = document.querySelector('#play');
  if (!back || !next || !play) return;

  back.setAttribute('aria-label', '前のコマ');
  next.setAttribute('aria-label', '次のコマ');

  var help = document.querySelector('.help');
  if (help) {
    var hint = document.createElement('p');
    hint.className = 'help keyboard-help';
    hint.textContent = 'キーボード：←・→でコマ送り、スペースで再生・停止。ボタンや入力欄を選択している間は、それぞれの通常操作になります。';
    help.insertAdjacentElement('afterend', hint);
  }

  function usesNativeKeys(target) {
    return target && (target.isContentEditable || target.closest(
      'input, textarea, select, button, a, summary, [contenteditable]:not([contenteditable="false"]), [role="button"], [role="slider"], [role="textbox"]'
    ));
  }

  document.addEventListener('keydown', function (event) {
    if (event.defaultPrevented || event.ctrlKey || event.altKey || event.metaKey || event.repeat || event.isComposing) return;
    if (usesNativeKeys(event.target) || usesNativeKeys(document.activeElement)) return;

    var control;
    if (event.key === 'ArrowLeft') control = back;
    else if (event.key === 'ArrowRight') control = next;
    else if (event.key === ' ' || event.key === 'Spacebar') control = play;
    if (!control || control.disabled) return;

    event.preventDefault();
    control.click();
  });
}());
