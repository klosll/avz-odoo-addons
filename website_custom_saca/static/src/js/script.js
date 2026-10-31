/** @odoo-module **/

// v18: portado desde el JS legacy v14 (odoo.define + require("web.ajax") + jQuery)
// a módulo ESM con fetch nativo. Mismo comportamiento: marcar checkboxes,
// alternar edición de la línea de saca, enviar la línea y subir imágenes.

function getCsrfToken() {
    const match = document.cookie.match(/(?:^|;\s*)csrf_token=([^;]+)/);
    return match ? match[1] : "";
}

function post(url, data) {
    // Paridad con web.ajax.post: envío tipo formulario con csrf_token
    const body = new FormData();
    for (const [key, value] of Object.entries(data)) {
        body.append(key, value);
    }
    body.append("csrf_token", getCsrfToken());
    return fetch(url, { method: "POST", body });
}

function checkCheckboxes() {
    document.querySelectorAll("input.checked").forEach((el) => {
        el.checked = true;
    });
}

function initSacaScripts() {
    checkCheckboxes();

    const btnEdit = document.getElementById("btn_saca_edit");
    const btnEdit2 = document.getElementById("btn_saca_edit_2");
    const btnSend = document.getElementById("btn_saca_send");
    const btnUpload = document.getElementById("upload_img");

    if (btnEdit2 && btnEdit) {
        btnEdit2.addEventListener("click", () => btnEdit.click());
    }

    if (btnEdit) {
        btnEdit.addEventListener("click", () => {
            const first = document.querySelector(".weight_input");
            const shown = first && getComputedStyle(first).display !== "none";
            const display = (sel, value) =>
                document.querySelectorAll(sel).forEach((el) => (el.style.display = value));
            if (!shown) {
                display(".info_span", "none");
                display(".weight_input", "block");
                display(".saca_input", "initial");
                display(".saca_input_file", "initial");
                display(".unload_input", "initial");
                display("#btn_saca_save", "block");
                display("#btn_saca_save_2", "block");
                display("#btn_saca_edit", "none");
                display("#btn_saca_edit_2", "none");
                display("#img_origin", "block");
                display("#img_dest", "block");
                const chbx = document.getElementById("chbx_fork");
                if (chbx) {
                    chbx.removeAttribute("disabled");
                }
            } else {
                display(".info_span", "block");
                display(".weight_input", "none");
                display(".unload_input", "none");
                display(".saca_input", "none");
                display(".saca_input_file", "none");
                document
                    .querySelectorAll(".chbx_fork")
                    .forEach((el) => el.setAttribute("disabled", "disabled"));
                display("#img_origin", "none");
                display("#img_dest", "none");
            }
        });
    }

    if (btnSend) {
        btnSend.addEventListener("click", () => {
            const id = btnSend.getAttribute("value");
            post(`/saca/line/send/${id}`, {}).then((result) => {
                console.log(result);
            });
        });
    }

    document.querySelectorAll(".ticket_upload").forEach((el) => {
        el.addEventListener("change", () => {
            console.log(el.previousElementSibling);
            if (el.previousElementSibling) {
                el.previousElementSibling.style.display = "block";
            }
        });
    });

    if (btnUpload) {
        btnUpload.addEventListener("click", () => {
            const fileInput = btnUpload.nextElementSibling;
            const sacaLineId = document.getElementById("current_saca_line")?.value;
            const data = {
                image_field: fileInput ? fileInput.getAttribute("name") : "",
            };
            if (fileInput && fileInput.files && fileInput.files.length) {
                data.image_file = fileInput.files[fileInput.files.length - 1];
            }
            post(`/my/saca/line/${sacaLineId}/binary`, data).then(() => {
                window.location.href = `/my/saca/line/${sacaLineId}`;
            });
        });
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSacaScripts);
} else {
    initSacaScripts();
}
