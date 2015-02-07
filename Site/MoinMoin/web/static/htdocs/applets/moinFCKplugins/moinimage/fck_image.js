/* FCKeditor - The text editor for internet
 * Copyright (C) 2003-2004 Frederico Caldeira Knabben
 * 
 * Licensed under the terms of the GNU Lesser General Public License:
 *   http://www.opensource.org/licenses/lgpl-license.php
 * 
 * For further information visit:
 *   http://www.fckeditor.net/
 * 
 * File Name: fck_image.js
 *  Scripts related to the Image dialog window
 * 
 * File Authors:
 *   Frederico Caldeira Knabben (fredck@fckeditor.net)
 *   Florian Festi
 */

var dialog	= window.parent ;
var oEditor  = window.parent.InnerDialogLoaded();
var FCK   = oEditor.FCK;
var FCKLang  = oEditor.FCKLang;
var FCKConfig = oEditor.FCKConfig;

var UriProtocol = new RegExp('');
UriProtocol.compile('^((http|https):\/\/|attachment:|drawing:|)', 'gi');
var UrlOnChangeProtocol = new RegExp('');
UrlOnChangeProtocol.compile('^(http|https)://(?=.)|attachment:|drawing:', 'gi');

var oImage = FCK.Selection.GetSelectedElement() ;
if ( oImage && oImage.tagName != 'IMG')
 oImage = null;

// Get the active link.
var oLink = dialog.Selection.GetSelection().MoveToAncestorNode( 'A' ) ;
if ( oLink )
	FCK.Selection.SelectNode( oLink ) ;

$(window).ready(function() {
  // Load the selected element information (if any).
  LoadSelection();

  // Update UI
  //OnProtocolChange();

  // select first text input element of dialog for usability
  //SelectField('txtUrl');
});

function LoadSelection()
{
  if (!oImage) return ;
  var sUrl = GetAttribute(oImage, 'src', '');
  var sTitle = GetAttribute(oImage, 'title', '');
  var sWidth = GetAttribute(oImage, 'width', '');
  var sHeight = GetAttribute(oImage, 'height', '');
  var sClass = GetAttribute(oImage, 'class', '');

  if (sTitle) sUrl = sTitle;

  // Search for the protocol.
  var sProtocol = UriProtocol.exec(sUrl);

  if (sProtocol)
  {
    sProtocol = sProtocol[0].toLowerCase();
    GetE('cmbLinkProtocol').value = sProtocol;

    // Remove the protocol and get the remainig URL.
    sUrl = sUrl.replace(UriProtocol, '');
  }
  
  $.ajax({
      url: FCKConfig['WikiBasePath'] + FCKConfig['WikiPage'] + "?action=imageDetail&name=" + sUrl, 
	  dataType: 'json', 
	  success: function(data){
		  imgs = data;
		  for(var i = 0; i < imgs.length; i++) {
		      img = imgs[i];
			  addImage(img, FCKConfig['WikiBasePath'] + FCKConfig['WikiPage'] + "?action=AttachFile&do=get&target=" + encodeURIComponent(img))
		  }
	  }
  });

  GetE('txtUrl').value = decodeURIComponent(sUrl);

  if (oLink) 
    GetE('chkLink').checked = 1;
  else
    GetE('chkLink').checked = 0;
	
   if(sWidth) {
       GetE('img_width').value = sWidth;
   }
   if(sHeight) {
       GetE('img_height').value = sHeight;
   }
   if(sClass.indexOf('floatLeft') >= 0) {
       GetE('image_align').value = 'floatLeft';
   }
   if(sClass.indexOf('floatRight') >= 0) {
       GetE('image_align').value = 'floatRight';
   }
   if(sClass.indexOf('center') >= 0) {
       GetE('image_align').value = 'center';
   }
}

function OnProtocolChange()
{ 
  var sProtocol = GetE('cmbLinkProtocol').value;
  ShowE('divChkLink', (sProtocol!='attachment:' && sProtocol!='drawing:'));
  // select first text input element of dialog for usability
  SelectField('txtUrl');
}

//#### Called while the user types the URL.
function OnUrlChange()
{
 var sUrl = GetE('txtUrl').value;
 var sProtocol = UrlOnChangeProtocol.exec(sUrl);

 if (sProtocol)
 {
  sUrl = sUrl.substr(sProtocol[0].length);
  GetE('txtUrl').value = sUrl;
  GetE('cmbLinkProtocol').value = sProtocol[0].toLowerCase();
 }
}

function getAttachUrl(sUrl)
{
  // XXX assumes attachments are not served directly!!!
  var iIdx = sUrl.lastIndexOf('/');
  var sPage = "";
  if (iIdx != -1)
  {
    sPage = sUrl.substring(0, iIdx);
    sUrl = sUrl.substring(iIdx+1, sUrl.length);
  } else
  {
    sPage = FCKConfig['WikiPage'];
  }
  return FCKConfig['WikiBasePath'] + sPage + 
          "?action=AttachFile&do=get&target=" + sUrl;
}

//#### The OK button was hit.
function Ok()
{
  var sPage = FCKConfig['WikiPage'];
  
  var images = []
  var imageElems = $(".ui-state-default img");
  for(var i = 0; i < imageElems.length; i++) {
      images.push(imageElems[i].getAttribute('_name'));
  }
  $.ajax({
     type: "POST", 
	 url: FCKConfig['WikiBasePath'] + sPage + "?action=createImage", 
	 data: {"name": GetE('txtUrl').value, "layout": JSON.stringify({"images": images, "width": GetE('img_width').value, "height": GetE('img_height').value})}, 
	 dataType: 'text', 
	 async: false,
	 success: function(data){
	     GetE('txtUrl').value = data;
	 }
  });

  if ( GetE('txtUrl').value.length == 0 )
  {
     window.parent.SetSelectedTab( 'Info' ) ;
     GetE('txtUrl').focus() ;
     alert( oEditor.FCKLang.DlgImgAlertUrl ) ;
     return false ;
  } 

  if (oImage==null)
  {
    oImage = FCK.CreateElement('IMG');
    oEditor.FCKSelection.SelectNode(oImage);
  }

  var sProtocol = GetE('cmbLinkProtocol').value;
  var sTitle = '';
  var sSrc = GetE('txtUrl').value;

  if (sProtocol!='drawing:')
  {
    // Check for valid image Url
    var sEnd = sSrc.substring(sSrc.length-4, sSrc.length).toLowerCase();
    if (!(sEnd==".gif" || sEnd=='.png' || sEnd=='.jpg' || sSrc.substring(sSrc.length-5, sSrc.length).toLowerCase()=='.jpeg'))
    {
      alert("Image Url must end with .gif, .png, .jpg or .jpeg"); //XXX i18n!
      return false;
    }
  }

  sTitle = sProtocol + encodeUrl(sSrc);
  sSrc = getAttachUrl(encodeUrl(sSrc));
  
  oImage.src = sSrc;
  oImage.title = sTitle;
  oImage.alt = sTitle.replace(sProtocol, '');
  oImage.width = GetE('img_width').value;
  oImage.height = GetE('img_height').value;
  if(GetE('image_align').value != 'none') {
      oImage.className = GetE('image_align').value;
      oImage.setAttribute('class', GetE('image_align').value);
  }
  
  window.parent.parent.adjust_img_paddings();

  return true;
}

function OnAttachmentListChange()
{
  var idx = GetE('sctAttachments').selectedIndex;
  GetE('txtUrl').value = GetE('sctAttachments').options[idx].value;
}
