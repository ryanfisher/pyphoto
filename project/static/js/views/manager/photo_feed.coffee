define ['cs!views/manager/photo_edit_view'], (PhotoManagerEditView) ->
  class PhotoManagerFeed extends Backbone.View
    el: '#photo-manager-feed'

    events:
      'click .delete-link': 'delete_photos'

    initialize: ->
      @photo_edit_views = []
      @render()

    render: ->
      @collection.on 'add', (model) =>
        @new_photo_view model
        @$('.feed').append @last_photo_view_el()
      @collection.once 'sync', =>
        @collection.off 'add'
        @collection.on 'add', (model) =>
          @new_photo_view model
          @$('.feed').prepend @last_photo_view_el()

    new_photo_view: (model) ->
      photo_edit_view = new PhotoManagerEditView({model})
      photo_edit_view.on 'selected_toggle', => @update_selected_count()
      @photo_edit_views.push photo_edit_view

    last_photo_view_el: ->
      @photo_edit_views[@photo_edit_views.length - 1].$el

    delete_photos: ->
      @delete_selected_photos()
      @update_selected_count()

    update_selected_count: ->
      selected_count = @$('.selected').length
      if selected_count > 0
        @$('.photos-selected').removeClass('hidden')
      else
        @$('.photos-selected').addClass('hidden')
      @$('.selected-count').text selected_count

    delete_selected_photos: ->
      to_delete = _.filter @photo_edit_views, (view) -> view.is_selected()
      delete_count = to_delete.length
      return if delete_count == 0
      confirm_text = "Are you sure you want to delete the selected photo(s)?" +
                     "\n\n#{delete_count} selected"
      if window.confirm(confirm_text)
        _.each to_delete, (view) -> view.delete_photo()
