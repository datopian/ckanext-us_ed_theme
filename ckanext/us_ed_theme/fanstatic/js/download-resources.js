$(document).ready(function () {

  var _ = ckan.i18n.ngettext;
  var downloadResourcesBtn = $('#download-resources');
  var resourceCheckboxes = $('input[name=mark-download-resource]');

  var clickLinkInBackground = function(url) {
    var link = document.createElement('a');
    link.style.display = 'none';
    link.href = url;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  var toggleDownloadButton = function(){
    setTimeout(function() {
      var $el = $(this);
      var atLeastOneChecked = false;

      $.each(resourceCheckboxes, function (i, el) {
        if (el.checked) {
          atLeastOneChecked = true;
        }
      });
      if (atLeastOneChecked) {
        downloadResourcesBtn.addClass('btn-success');
        downloadResourcesBtn.removeAttr('disabled');
      } else {
        downloadResourcesBtn.removeClass('btn-success');
        downloadResourcesBtn.attr('disabled', 'disabled');
      }
    }, 0)
  };

  // When the Mark All button is clicked, toggle the state for checkboxes displayed next to each resource
  $('.btn-mark-all').click(function (e) {
    toggleDownloadButton()
  });

  // Disable/enable the Download button depending if any checkbox is checked.
  resourceCheckboxes.click(function (e) {
    toggleDownloadButton();
  });

  downloadResourcesBtn.click(function (e) {
    var url = window.location.origin + '/api/action/us_ed_theme_prepare_zip_resources';
    var data = { resources: [] };

    downloadResourcesBtn.attr('disabled', 'disabled');
    downloadResourcesBtn.text(_('Preparing zip archive...'));

    $.each(resourceCheckboxes, function (i, el) {
      if (el.checked) {
        data.resources.push(el.value);
      }
    });

    $.post(url, JSON.stringify(data), function (response) {
      var zip_id = response.result.zip_id;

      downloadResourcesBtn.removeAttr('disabled');
      downloadResourcesBtn.text(_('Download'));

      if (zip_id) {
        var link = document.createElement('a');
        url = window.location.origin + '/download/zip/' + zip_id;
        link.style.display = 'none';
        link.href = url;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        window.ckan.notify(_('Could not create a zip archive.'));
      }
    }).error(function (response) {
      downloadResourcesBtn.removeAttr('disabled');
      downloadResourcesBtn.text(_('Download'));

      window.ckan.notify(_('An error occured while preparing zip archive.'));
    });
  });

  toggleDownloadButton(); // first time we load.
});
