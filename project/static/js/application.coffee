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
], (UserPhotos, PhotoManager, ManagerRouter, PhotoFeed) ->

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

  jQuery('document').ready ->
    App = new App()
