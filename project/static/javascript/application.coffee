class PhotoManager extends Backbone.View
  el: '#photo-manager'

  events:
    'click .delete-link': 'delete_photos'

  initialize: ->
    new Uploader({@collection})
    @photo_feed = new PhotoManagerFeed({@collection})

  delete_photos: (event) ->
    event.preventDefault()
    @photo_feed.delete_selected_photos()

class PhotoManagerEditView extends Backbone.View
  className: 'photo'

  initialize: ->
    thumbnail_url = "url(#{@model.get('thumbnail_url')})".replace /\s/, "%20"
    @$el.css('background-image', thumbnail_url)
    @$el.append($('<input>', type: 'checkbox'))

  # Checks if photo is selected
  #
  # @return [Boolean]
  is_checked: ->
    @$('input').is(':checked') and @$el.is(':visible')

  delete_photo: ->
    @model.destroy()
    @remove()

class PhotoManagerFeed extends Backbone.View
  el: '#photo-manager-feed'

  initialize: ->
    @photo_edit_views = []
    @collection.on 'add', (model) =>
      photo_edit_view = new PhotoManagerEditView({model})
      @photo_edit_views.push photo_edit_view
      @$el.append(photo_edit_view.$el)
    @collection.once 'sync', =>
      @collection.off 'add'
      @collection.on 'add', (model) =>
        photo_edit_view = new PhotoManagerEditView({model})
        @photo_edit_views.push photo_edit_view
        @$el.prepend(photo_edit_view.$el)

  delete_selected_photos: ->
    to_delete = _.filter @photo_edit_views, (view) -> view.is_checked()
    delete_count = to_delete.length
    return if delete_count == 0
    confirm_text = "Are you sure you want to delete the selected photo(s)?" +
                   "\n\n#{delete_count} selected"
    if window.confirm(confirm_text)
      _.each to_delete, (view) -> view.delete_photo()

class Uploader extends Backbone.View
  el: "#uploader"

  events:
    'submit form' : "upload_photos"

  initialize: ->
    $('#id_file').hide()
    @uploading = false

  upload_photos: ->
    event.preventDefault()
    return if @uploading
    @uploading = true
    form = $(event.target)
    file_input = form.find('[type="file"]:visible')
    for photo_file in file_input[0].files
      info = new ProgressInfo
      @send_request(photo_file, info)

  send_request: (photo_file, progress_info)->
    info = progress_info
    form_data = new FormData()
    form_data.append('file', photo_file)
    csrf_token = @$('input[name="csrfmiddlewaretoken"]').val()
    $.ajax
      type: "POST"
      url: "/upload"
      data: form_data
      headers: 'X-CSRFToken': csrf_token
      success: (data) =>
        @collection.add data
        info.display_message(200)
      error: (jqXHR) -> info.display_message(jqXHR.status)
      complete: =>
        info.stop_animation()
        @uploading = false;
        @$('form')[0].reset();
      processData: false,
      contentType: false,
      xhr: ->
        myXhr = $.ajaxSettings.xhr();
        if myXhr.upload
          callback = (ev) ->
            if ev.lengthComputable
              percentUploaded = Math.floor(ev.loaded * 100 / ev.total)
              info.update_bar(percentUploaded)
          myXhr.upload.addEventListener 'progress', callback, false
        myXhr

class ProgressInfo extends Backbone.View
  className: 'progress-info'

  events:
    'click': 'remove_if_done'

  initialize: ->
    @bar = $('<div>', class: 'bar animated')
    progress = $('<div>', class: 'progress').append(@bar)
    @$el.append(progress)
    @message = $('<p>', class: 'message')
    @$el.append(@message)
    $('#progress-bars').prepend(@$el)

  update_bar: (percent_uploaded) ->
    @bar.css('width', "#{percent_uploaded}%")

  display_message: (status) ->
    message = switch status
      when 200 then 'success'
      when 409 then 'error409'
      else 'error'
    @message.addClass(message).text($('#progress-bars').data(message))

  stop_animation: ->
    @bar.removeClass('animated')

  remove_if_done: ->
    return if @bar.hasClass('animated')
    @remove()

class PhotoFeed extends Backbone.View
  el: '#photo-feed'

  initialize: ->
    @collection.on 'add', (model) =>
      photo_view = new PhotoView({model})
      @$el.append(photo_view.$el)

class PhotoImg extends Backbone.View
  tagName: 'img'

  initialize: ->
    @$el.attr('src', @model.get('thumbnail_url'))

class PhotoView extends Backbone.View
    tagName: 'a'
    className: 'photo'

    initialize: ->
      @$el.attr('href', "/photos/#{@model.get('id')}")
      img = new PhotoImg({@model})
      @$el.append(img.$el)

class UserPhoto extends Backbone.Model

class UserPhotos extends Backbone.Collection
  url: '/api/photos'
  model: UserPhoto

class App extends Backbone.View

  initialize: ->
    collection = new UserPhotos
    new PhotoFeed({collection}) if $('#photo-feed').length
    new PhotoManager({collection}) if $('#photo-manager').length
    collection.fetch()

jQuery('document').ready ->
  App = new App()
