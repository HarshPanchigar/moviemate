// ---------- AUTH & FORM HELPER UTILITIES ----------
function toggleEye(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;

  const isPassword = input.type === 'password';
  input.type = isPassword ? 'text' : 'password';
  if (btn) {
    btn.textContent = isPassword ? 'HIDE' : 'SHOW';
  }
}

function togglePassword(inputId, button) {
  toggleEye(inputId, button);
}

function toggleDeleteButton() {
  const checkbox = document.getElementById("confirm-delete");
  const button = document.getElementById("delete-button");
  if (!checkbox || !button) return;

  if (checkbox.checked) {
    button.disabled = false;
    button.classList.add("ready");
  } else {
    button.disabled = true;
    button.classList.remove("ready");
  }
}
