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
      collection = new UserPhotos
      new PhotoFeed({collection}) if $('#photo-feed').length
      if $('#photo-manager').length
        new PhotoManager({collection})
        router = new ManagerRouter
        Backbone.history.start()
      collection.fetch()

  jQuery('document').ready ->
    App = new App()
