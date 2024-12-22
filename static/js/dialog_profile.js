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

; (function () {

  const modal4 = new bootstrap.Modal(document.getElementById("edit_pfp_modal"))

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "edit_pfp_dialog") {
      modal4.show()
    }
  })

  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "edit_pfp_dialog" && !e.detail.xhr.response) {
      modal4.hide()
      e.detail.shouldSwap = false
    }
  })

  // Remove dialog content after hiding
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("edit_pfp_dialog").innerHTML = ""
  })
})()
  