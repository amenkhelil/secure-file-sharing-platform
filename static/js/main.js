/**
 * main.js — SecureShare Frontend
 * Handles: mobile nav toggle, flash message auto-dismiss,
 *          drag-and-drop upload zone, file selection preview,
 *          copy-to-clipboard for share links, and delete confirmation.
 */

/* =========================================================
   1. Mobile Navigation Toggle
   ========================================================= */
(function () {
  var toggle = document.getElementById('navToggle');
  var mobileMenu = document.getElementById('navMobile');

  if (toggle && mobileMenu) {
    toggle.addEventListener('click', function () {
      var isOpen = mobileMenu.classList.contains('nav-mobile-open');
      if (isOpen) {
        mobileMenu.classList.remove('nav-mobile-open');
        toggle.setAttribute('aria-expanded', 'false');
      } else {
        mobileMenu.classList.add('nav-mobile-open');
        toggle.setAttribute('aria-expanded', 'true');
      }
    });

    // Close mobile menu when a link is clicked
    mobileMenu.querySelectorAll('.nav-mobile-link').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileMenu.classList.remove('nav-mobile-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
})();


/* =========================================================
   2. Auto-dismiss Flash Messages (after 5 seconds)
   ========================================================= */
(function () {
  var flashes = document.querySelectorAll('.flash');
  flashes.forEach(function (flash) {
    setTimeout(function () {
      if (flash && flash.parentElement) {
        flash.style.transition = 'opacity 0.4s ease';
        flash.style.opacity = '0';
        setTimeout(function () {
          if (flash.parentElement) {
            flash.parentElement.removeChild(flash);
          }
        }, 400);
      }
    }, 5000);
  });
})();


/* =========================================================
   3. File Upload Zone (drag & drop + file picker)
   ========================================================= */
(function () {
  var dropZone   = document.getElementById('dropZone');
  var fileInput  = document.getElementById('fileInput');
  var filePreview   = document.getElementById('filePreview');
  var previewName   = document.getElementById('filePreviewName');
  var clearBtn      = document.getElementById('clearFile');
  var uploadBtn     = document.getElementById('uploadBtn');
  var dropZoneContent = dropZone ? dropZone.querySelector('.drop-zone-content') : null;

  if (!dropZone || !fileInput) return; // Only run on the files page

  /* --- Helper: show selected file name --- */
  function showPreview(filename) {
    if (previewName) previewName.textContent = filename;
    if (filePreview) filePreview.style.display = 'flex';
    if (dropZoneContent) dropZoneContent.style.display = 'none';
    if (uploadBtn) uploadBtn.disabled = false;
  }

  /* --- Helper: reset the zone --- */
  function clearSelection() {
    fileInput.value = '';
    if (filePreview) filePreview.style.display = 'none';
    if (dropZoneContent) dropZoneContent.style.display = '';
    if (uploadBtn) uploadBtn.disabled = true;
    dropZone.classList.remove('drop-zone-active');
  }

  /* --- File input change (click "Choose File") --- */
  fileInput.addEventListener('change', function () {
    if (fileInput.files && fileInput.files.length > 0) {
      showPreview(fileInput.files[0].name);
    }
  });

  /* --- Clear button --- */
  if (clearBtn) {
    clearBtn.addEventListener('click', clearSelection);
  }

  /* --- Drag events --- */
  ['dragenter', 'dragover'].forEach(function (evt) {
    dropZone.addEventListener(evt, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('drop-zone-active');
    });
  });

  ['dragleave', 'dragend'].forEach(function (evt) {
    dropZone.addEventListener(evt, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('drop-zone-active');
    });
  });

  dropZone.addEventListener('drop', function (e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drop-zone-active');

    var files = e.dataTransfer.files;
    if (!files || files.length === 0) return;

    var file = files[0];

    // Validate extension client-side (same list as backend)
    var allowed = ['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'];
    var ext = file.name.split('.').pop().toLowerCase();
    if (allowed.indexOf(ext) === -1) {
      showTemporaryError('File type not allowed. Use: PDF, DOCX, TXT, PNG, JPG, JPEG.');
      return;
    }

    // Validate size client-side (20 MB)
    if (file.size > 20 * 1024 * 1024) {
      showTemporaryError('File is too large. Maximum size is 20 MB.');
      return;
    }

    // Assign the dropped file to the input
    try {
      var dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      fileInput.files = dataTransfer.files;
    } catch (err) {
      // DataTransfer not supported — tell the user to use the picker instead
      showTemporaryError('Drag & drop not fully supported in this browser. Please use the "Choose File" button.');
      return;
    }

    showPreview(file.name);
  });

  /* --- Show a temporary inline error near the drop zone --- */
  function showTemporaryError(msg) {
    var existing = dropZone.parentElement.querySelector('.drop-zone-error');
    if (existing) existing.parentElement.removeChild(existing);

    var err = document.createElement('p');
    err.className = 'drop-zone-error';
    err.style.cssText = 'color:#e53e3e;font-size:0.85rem;margin-top:0.5rem;';
    err.textContent = msg;
    dropZone.parentElement.insertBefore(err, dropZone.nextSibling);

    setTimeout(function () {
      if (err.parentElement) err.parentElement.removeChild(err);
    }, 4000);
  }
})();


/* =========================================================
   4. Copy Share Link to Clipboard
   Defined as a global function because it is called from
   inline onclick="" attributes in files.html
   ========================================================= */
function copyLink(inputId) {
  var input = document.getElementById(inputId);
  if (!input) return;

  // Modern clipboard API
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(input.value).then(function () {
      showCopiedFeedback(input);
    }).catch(function () {
      fallbackCopy(input);
    });
  } else {
    fallbackCopy(input);
  }
}

function fallbackCopy(input) {
  input.select();
  input.setSelectionRange(0, 9999); // mobile
  try {
    document.execCommand('copy');
    showCopiedFeedback(input);
  } catch (err) {
    // Silent fail — user can manually copy from the input
  }
}

function showCopiedFeedback(input) {
  // Find the Copy button next to this input and temporarily change its text
  var btn = input.nextElementSibling;
  if (btn && btn.tagName === 'BUTTON') {
    var original = btn.textContent;
    btn.textContent = 'Copied!';
    btn.disabled = true;
    setTimeout(function () {
      btn.textContent = original;
      btn.disabled = false;
    }, 2000);
  }
}