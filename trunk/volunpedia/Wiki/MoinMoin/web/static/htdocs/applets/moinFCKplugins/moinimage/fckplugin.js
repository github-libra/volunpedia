var noImage = /^(?:H1|H2|H3|H4|H5|H6|PRE|TT|A)$/i;

function ImageState()
{
  oImg = FCKSelection.GetSelectedElement();
  if (oImg && oImg.nodeName=='IMG')
  {
    var sUrl = oImg.getAttribute('src', '');
    if (sUrl.substring(0, FCKConfig['SmileyPath'].length)==
        FCKConfig['SmileyPath']) 
      return FCK_TRISTATE_DISABLED;
  } 
  return FCK_TRISTATE_OFF;
}

if (1 || !FCKBrowserInfo.IsIE){

// Register the related command.
FCKCommands.RegisterCommand('Image', new FCKDialogCommand( 'Image', FCKLang.DlgImgTitle, FCKConfig.WikiBasePath + FCKConfig.WikiPage + '?action=fckdialog&dialog=image', 400, 480, ImageState, 'Image')) ;

// add icon location on strip file(theme/silver/fck_strip.gif)
FCKToolbarItems.RegisterItem('Image', new FCKToolbarButton
  ('Image', FCKLang.InsertImageLbl, FCKLang.InsertImage, null, false, true, 37));

}
else
{
FCKCommands.RegisterCommand('Image', new FCKDialogCommand( 'Image', FCKLang.DlgImgTitle, FCKConfig.WikiBasePath + FCKConfig.WikiPage + '?action=fckdialog&dialog=image', 400, 480, FCK.GetNamedCommandState, 'Image')) ;
}
