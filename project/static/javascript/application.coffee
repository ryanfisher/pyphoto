(->
  _sync = Backbone.sync
  Backbone.sync = (method, model, options) ->
    options.beforeSend = (xhr) ->
      token = $('meta[name="csrf-token"]').attr("content")
      xhr.setRequestHeader "X-CSRFToken", token
      return
    _sync method, model, options
)()

class AlbumEditor extends Backbone.View
  el: '#album-editor'

  events:
    'click h4': 'toggle_open'
    'click #new-album': 'open_new_album_form'
    'submit form': 'save_album'

  initialize: ->
    @collection.fetch success: => @render()

  render: ->
    @collection.each (album) ->
      @$('.albums').prepend($('<a>', text: album.get('title')))
    @collection.on 'add', (album) =>
      @$('.albums').prepend($('<a>', text: album.get('title')))

  open_new_album_form: ->
    @$('form').removeClass('hidden')
    @$('button').addClass('hidden')

  save_album: ->
    event.preventDefault()
    input = @$('input[name=title]')
    @$('form').addClass('hidden')
    @$('button').removeClass('hidden')
    @collection.create title: input.val()
    input.val('')

  toggle_open: ->
    @$('.album-editor').toggleClass('hidden')

class UserAlbum extends Backbone.Model

class UserAlbums extends Backbone.Collection
  url: '/api/albums'
  model: UserAlbum

class PhotoManager extends Backbone.View
  el: '#photo-manager'

  events:
    'click .delete-link': 'delete_photos'

  initialize: ->
    @uploader = new Uploader({@collection})
    collection = new UserAlbums
    @album_editor = new AlbumEditor({collection})
    @photo_feed = new PhotoManagerFeed({@collection})

  delete_photos: (event) ->
    event.preventDefault()
    @photo_feed.delete_selected_photos()

class PhotoManagerEditView extends Backbone.View
  className: 'photo hidden'

  events:
    'click': 'toggle_selected'

  initialize: ->
    img_url = @model.get('thumbnail_url')
    # Load image before showing it in view
    $('<img>', src: img_url).on 'load', => @$el.removeClass('hidden')
    thumbnail_url = "url(#{img_url})".replace /\s/, "%20"
    @$el.css('background-image', thumbnail_url)

  # Checks if photo is selected
  #
  # @return [Boolean]
  is_selected: ->
    @$el.is(':visible') and @$el.hasClass('selected')

  toggle_selected: ->
    @$el.toggleClass('selected')

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
    to_delete = _.filter @photo_edit_views, (view) -> view.is_selected()
    delete_count = to_delete.length
    return if delete_count == 0
    confirm_text = "Are you sure you want to delete the selected photo(s)?" +
                   "\n\n#{delete_count} selected"
    if window.confirm(confirm_text)
      _.each to_delete, (view) -> view.delete_photo()

class Uploader extends Backbone.View
  el: "#uploader"

  events:
    'click h4': 'toggle_open'
    'change input': 'upload_photos'

  initialize: ->
    $('#id_file').hide()
    @uploading = false

  toggle_open: ->
    @$('form').toggleClass('hidden')

  upload_photos: ->
    return if @uploading
    @uploading = true
    for photo_file in @$('.multiple-photos')[0].files
      info = new ProgressInfo(photo_file)
      @send_request(photo_file, info)

  send_request: (photo_file, progress_info)->
    info = progress_info
    form_data = new FormData()
    form_data.append('file', photo_file)
    csrf_token = @$('input[name="csrfmiddlewaretoken"]').val()
    $.ajax
      type: "POST"
      url: "/api/photos"
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

  initialize: (@file) ->
    @bar = $('<div>', class: 'bar animated')
    progress = $('<div>', class: 'progress').append(@bar)
    @$el.append(progress)
    uploading_text = $('#progress-bars').data('uploading-message')
    @message = $('<p>', class: 'message', text: uploading_text + @file.name)
    @$el.prepend(@message)
    $('#progress-bars').prepend(@$el)

  update_bar: (percent_uploaded) ->
    @bar.css('width', "#{percent_uploaded}%")

  display_message: (status) ->
    message = switch status
      when 200 then 'success'
      when 409 then 'error409'
      else 'error'
    display_text = $('#progress-bars').data(message)
    @message.addClass(message).text(display_text + @file.name)

  stop_animation: ->
    @bar.removeClass('animated')

  remove_if_done: ->
    return if @bar.hasClass('animated')
    @remove()

class PhotoFeed extends Backbone.View
  el: '#photo-feed'

  PHOTO_HEIGHT = 250
  USE_COLUMNS = true

  initialize: ->
    @set_up_columns() if USE_COLUMNS
    @collection.on 'add', (model) =>
      photo_view = new PhotoView({model})
      if USE_COLUMNS
        photo_view.set_width(@columns[0].get_width())
        @columns[@current_col].append(photo_view)
        @current_col++
        @current_col = 0 if @current_col == @columns.length
      else
        photo_view.set_height(PHOTO_HEIGHT)
        @$el.append(photo_view.$el)

  set_up_columns: ->
    @current_col = 0
    column_count = 4
    width = $(window).width() / column_count
    @columns = []
    for i in [1..column_count]
      col = new PhotoColumn
      col.set_width(width-8)
      @columns.push(col)
      @$el.append(col.$el)

class PhotoColumn extends Backbone.View
  className: 'column'

  set_width: (width) ->
    console.log width
    @$el.width(width)
    @width = width

  get_width: -> @width

  append: (view) -> @$el.append(view.$el)

class PhotoImg extends Backbone.View
  tagName: 'img'
  className: 'hidden'

  initialize: ->
    @$el.on 'load', => @$el.removeClass('hidden')
    @$el.attr('src', @model.get('thumbnail_url'))

class PhotoView extends Backbone.View
  tagName: 'a'
  className: 'photo'

  initialize: ->
    @$el.attr('href', "/photos/#{@model.get('id')}")
    img = new PhotoImg({@model})
    @$el.append(img.$el)

  set_height: (height) ->
    @$el.height(height)
    @$el.width(@model.width_from(height))

  set_width: (width) ->
    @$el.width(width)
    @$el.height(@model.height_from(width))

class UserPhoto extends Backbone.Model
  height_from: (width) ->
    width * @get('height') / @get('width')

  width_from: (height) ->
    height * @get('width') / @get('height')

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
