
class Uploader extends Backbone.View
  el: "#uploader"

  events:
    'submit form' : "upload_photo"

  initialize: ->
    @uploading = false

  upload_photo: ->
    event.preventDefault()
    return if @uploading
    @info = @$('.progress-info').first().clone()
    @$el.append(@info)
    progress_bar = @info.find('.progress')
    progress_bar.show()
    @uploading = true
    form = $(event.target)
    file_input = form.find('#id_file')
    photo_file = file_input[0].files[0]
    form_data = new FormData()
    form_data.append('file', photo_file)
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax
      type: "POST"
      url: "/upload"
      data: form_data
      headers: 'X-CSRFToken': csrf_token
      success: (data) => @info.find('.success').show()
      error: (jqXHR) =>
        if jqXHR.status == 409
          @info.find('.error409').show()
        else
          @info.find('.failure').show()
      complete: =>
        @uploading = false;
        form[0].reset();
      processData: false,
      contentType: false,
      xhr: ->
        myXhr = $.ajaxSettings.xhr();
        if myXhr.upload
          callback = (ev) ->
            if ev.lengthComputable
              percentUploaded = Math.floor(ev.loaded * 100 / ev.total)
              console.info('Uploaded '+percentUploaded+'%')
              progress_bar.find('.bar').css('width', percentUploaded+'%')
            else
              console.info('Uploaded '+ev.loaded+' bytes')
          myXhr.upload.addEventListener 'progress', callback, false
        myXhr


class AppView extends Backbone.View

  initialize: -> new Uploader()

jQuery('document').ready ->
  App = new AppView()
