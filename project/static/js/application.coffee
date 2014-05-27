(->
  _sync = Backbone.sync
  Backbone.sync = (method, model, options) ->
    options.beforeSend = (xhr) ->
      token = $('meta[name="csrf-token"]').attr("content")
      xhr.setRequestHeader "X-CSRFToken", token
      return
    _sync method, model, options
)()

define [
  'cs!collections/user_photos'
  'cs!views/photo_manager'
  'cs!routers/manager_router'
  'cs!views/photo_feed'
  'cs!views/photo_page'
  'cs!models/user_photo'
], (UserPhotos, PhotoManager, ManagerRouter, PhotoFeed, PhotoPage, UserPhoto) ->

  class App extends Backbone.View

    initialize: ->
      if bootstrapped_photos? and $('#photo-feed').length
        collection = new UserPhotos(bootstrapped_photos)
        new PhotoFeed({collection})
      if $('#photo-manager').length
        collection = new UserPhotos
        new PhotoManager({collection})
        collection.fetch()
        router = new ManagerRouter
        Backbone.history.start()
      if bootstrapped_photo?
        model = new UserPhoto(bootstrapped_photo)
        new PhotoPage({model})
      if $('#login-background').length
        bg_path = '/static/images/barcelona_background.jpg'
        $('<img>', src: bg_path).load ->
          $('#login-background img').attr('src', bg_path).
            addClass('loaded')

  jQuery('document').ready ->
    App = new App()
