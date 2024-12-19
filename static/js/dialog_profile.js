; (function () {

    const modal3 = new bootstrap.Modal(document.getElementById("edit_email_modal"))
  
    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "edit_email_dialog") {
        modal3.show()
      }
    })
  
    htmx.on("htmx:beforeSwap", (e) => {
      // Empty response targeting #dialog => hide the modal
      if (e.detail.target.id == "edit_email_dialog" && !e.detail.xhr.response) {
        modal3.hide()
        e.detail.shouldSwap = false
      }
    })
  
    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("edit_email_dialog").innerHTML = ""
    })
  })()
  