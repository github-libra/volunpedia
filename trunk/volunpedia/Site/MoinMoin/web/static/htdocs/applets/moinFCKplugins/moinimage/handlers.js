function preLoad() {
	if (!this.support.loading) {
		alert("You need the Flash Player 9.028 or above to use SWFUpload.");
		return false;
	}
}
function loadFailed() {
	alert("Something went wrong while loading SWFUpload. If this were a real application we'd clean up and then give you an alternative");
}

function fileQueueError(file, errorCode, message) {
	try {
		var imageName = "error.gif";
		var errorName = "";
		if (errorCode === SWFUpload.errorCode_QUEUE_LIMIT_EXCEEDED) {
			errorName = "You have attempted to queue too many files.";
		}

		if (errorName !== "") {
			alert(errorName);
			return;
		}

		switch (errorCode) {
		case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
			imageName = "zerobyte.gif";
			break;
		case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:
			imageName = "toobig.gif";
			break;
		case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
		case SWFUpload.QUEUE_ERROR.INVALID_FILETYPE:
		default:
			alert(message);
			break;
		}

		addImage("images/" + imageName, "images/" + imageName);

	} catch (ex) {
		this.debug(ex);
	}

}

function fileDialogComplete(numFilesSelected, numFilesQueued) {
	try {
		if (numFilesQueued > 0) {
			this.startResizedUpload(this.getFile(0).ID, 800, 800, SWFUpload.RESIZE_ENCODING.JPEG, 100);
		}
	} catch (ex) {
		this.debug(ex);
	}
}

function uploadProgress(file, bytesLoaded) {
    document.getElementById("divFileProgressContainer").style.display = '';
	try {
		var percent = Math.ceil((bytesLoaded / file.size) * 100);

		var progress = new FileProgress(file,  this.customSettings.upload_target);
		progress.setProgress(percent);
		progress.setStatus("上传中...");
		progress.toggleCancel(true, this);
	} catch (ex) {
		this.debug(ex);
	}
}

function uploadSuccess(file, serverData) {
	try {
		var progress = new FileProgress(file,  this.customSettings.upload_target);

		if (serverData.substring(0, 7) === "FILEID:") {
		    var idx = serverData.indexOf('|FILENAME:');
			var url = serverData.substring(7, idx);
			var name = serverData.substring(idx + 10);
			addImage(name, url);
			
			var exists = false;
			var imageSelector = document.getElementById('imageList');
			var options = imageSelector.options;
			for(var i = 0; i < options.length; i++) {
			    if(options[i].value == url) {
				    exists = true;
				}
			}
			if(!exists) {
			    newOption = document.createElement('option');
				newOption.setAttribute('_name', name);
				newOption.innerHTML = name;
				newOption.value = url;
				imageSelector.appendChild(newOption);
			}

			progress.setStatus("上传结束。");
			progress.toggleCancel(false);
		} else {
			addImage("images/error.gif", "images/error.gif");
			progress.setStatus("Error.");
			progress.toggleCancel(false);
			alert(serverData);

		}


	} catch (ex) {
		this.debug(ex);
	}
}

function uploadComplete(file) {
	try {
		/*  I want the next upload to continue automatically so I'll call startUpload here */
		if (this.getStats().files_queued > 0) {
			this.startResizedUpload(this.getFile(0).ID, 800, 800, SWFUpload.RESIZE_ENCODING.JPEG, 100);
		} else {
			var progress = new FileProgress(file,  this.customSettings.upload_target);
			progress.setComplete();
			progress.setStatus("所有图片上传成功。");
			progress.toggleCancel(false);
			document.getElementById("divFileProgressContainer").style.display = 'none';
		}
	} catch (ex) {
		this.debug(ex);
	}
}

function uploadError(file, errorCode, message) {
	var imageName =  "error.gif";
	var progress;
	try {
		switch (errorCode) {
		case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:
			try {
				progress = new FileProgress(file,  this.customSettings.upload_target);
				progress.setCancelled();
				progress.setStatus("Cancelled");
				progress.toggleCancel(false);
			}
			catch (ex1) {
				this.debug(ex1);
			}
			break;
		case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:
			try {
				progress = new FileProgress(file,  this.customSettings.upload_target);
				progress.setCancelled();
				progress.setStatus("Stopped");
				progress.toggleCancel(true);
			}
			catch (ex2) {
				this.debug(ex2);
			}
		case SWFUpload.UPLOAD_ERROR.UPLOAD_LIMIT_EXCEEDED:
			imageName = "uploadlimit.gif";
			break;
		default:
			alert(message);
			break;
		}

		addImage("images/" + imageName, "images/" + imageName);

	} catch (ex3) {
		this.debug(ex3);
	}

}

thumbnails = []
function addImage(name, src) {
    for(var i = 0; i < thumbnails.length; i++) {
	    if(thumbnails[i].src == src) {
		    return;
		}
	}
	thumbnails.push({name: name, src: src});
	if(thumbnails.length > 0) {
	    document.getElementById('nextPageButton').disabled = false;
	}
	
	var newImg = document.createElement("img");
	newImg.style.margin = "5px";
	newImg.style.width = "65px";
	newImg.style.height = "65px";
	
	newImg.setAttribute('_src', src);
	$(newImg).click(function(){
	    document.getElementById("thumbnails").removeChild(this);
		for(var i = 0; i < thumbnails.length; i++) {
	        if(thumbnails[i].src == this.getAttribute('_src')) {
			    var t = [];
				for(var j = 0; j < thumbnails.length; j++) {
				    if(j != i) {
					    t.push(thumbnails[j]);
					}
				}
			    thumbnails = t;
				if(thumbnails.length == 0) {
					document.getElementById('nextPageButton').disabled = true;
				}
				return;
		    }
	    }
	});

	document.getElementById("thumbnails").appendChild(newImg);
	if (newImg.filters) {
		try {
			newImg.filters.item("DXImageTransform.Microsoft.Alpha").opacity = 0;
		} catch (e) {
			// If it is not set initially, the browser will throw an error.  This will set it if it is not set yet.
			newImg.style.filter = 'progid:DXImageTransform.Microsoft.Alpha(opacity=' + 0 + ')';
		}
	} else {
		newImg.style.opacity = 0;
	}

	newImg.onload = function () {
		fadeIn(newImg, 0);
	};
	newImg.src = src;
}

function layoutImage(id, width, height) {
    var cols = 2;
	if(thumbnails.length > 4) {
	    cols = 3;
	}
	if(thumbnails.length == 1) {
	    cols = 1;
	}
	rows = Math.ceil(thumbnails.length / cols);
	picWidth = Math.floor((width - (cols - 1) * 3) / cols);
	picHeight = Math.floor((height - (rows - 1) * 3) / rows);
	
	var container = document.getElementById(id);
	container.innerHTML = '';
	for(var i = 0; i < thumbnails.length; i++) {
	    var li = document.createElement('li');
		$(li).addClass('ui-state-default');
		li.style.float = 'left';
		li.style.display = 'inline';
		li.style.width = picWidth + 'px';
		li.style.margin = '3px';
		li.setAttribute('title', thumbnails[i].name);
		container.appendChild(li);
		
	    var img = document.createElement('img');
		img.src = thumbnails[i].src;
		img.setAttribute('_name', thumbnails[i].name);
		img.style.width = picWidth + 'px';
		img.style.height = picHeight + 'px';
		li.appendChild(img);
	}
	
	$(".ui-state-default").bind('mouseover',function(){ 
        $(this).css("cursor","move") 
    }); 
	
	$("#" + id).sortable();
	$("#" + id).disableSelection();
}

function fadeIn(element, opacity) {
	var reduceOpacityBy = 5;
	var rate = 30;	// 15 fps


	if (opacity < 100) {
		opacity += reduceOpacityBy;
		if (opacity > 100) {
			opacity = 100;
		}

		if (element.filters) {
			try {
				element.filters.item("DXImageTransform.Microsoft.Alpha").opacity = opacity;
			} catch (e) {
				// If it is not set initially, the browser will throw an error.  This will set it if it is not set yet.
				element.style.filter = 'progid:DXImageTransform.Microsoft.Alpha(opacity=' + opacity + ')';
			}
		} else {
			element.style.opacity = opacity / 100;
		}
	}

	if (opacity < 100) {
		setTimeout(function () {
			fadeIn(element, opacity);
		}, rate);
	}
}



/* ******************************************
 *	FileProgress Object
 *	Control object for displaying file info
 * ****************************************** */

function FileProgress(file, targetID) {
	this.fileProgressID = "divFileProgress";

	this.fileProgressWrapper = document.getElementById(this.fileProgressID);
	if (!this.fileProgressWrapper) {
		this.fileProgressWrapper = document.createElement("div");
		this.fileProgressWrapper.className = "progressWrapper";
		this.fileProgressWrapper.id = this.fileProgressID;

		this.fileProgressElement = document.createElement("div");
		this.fileProgressElement.className = "progressContainer";

		var progressCancel = document.createElement("a");
		progressCancel.className = "progressCancel";
		progressCancel.href = "#";
		progressCancel.style.visibility = "hidden";
		progressCancel.appendChild(document.createTextNode(" "));

		var progressText = document.createElement("div");
		progressText.className = "progressName";
		progressText.appendChild(document.createTextNode(file.name));

		var progressBar = document.createElement("div");
		progressBar.className = "progressBarInProgress";

		var progressStatus = document.createElement("div");
		progressStatus.className = "progressBarStatus";
		progressStatus.innerHTML = "&nbsp;";

		this.fileProgressElement.appendChild(progressCancel);
		this.fileProgressElement.appendChild(progressText);
		this.fileProgressElement.appendChild(progressStatus);
		this.fileProgressElement.appendChild(progressBar);

		this.fileProgressWrapper.appendChild(this.fileProgressElement);

		document.getElementById(targetID).appendChild(this.fileProgressWrapper);
		fadeIn(this.fileProgressWrapper, 0);

	} else {
		this.fileProgressElement = this.fileProgressWrapper.firstChild;
		this.fileProgressElement.childNodes[1].firstChild.nodeValue = file.name;
	}

	this.height = this.fileProgressWrapper.offsetHeight;

}
FileProgress.prototype.setProgress = function (percentage) {
	this.fileProgressElement.className = "progressContainer green";
	this.fileProgressElement.childNodes[3].className = "progressBarInProgress";
	this.fileProgressElement.childNodes[3].style.width = percentage + "%";
};
FileProgress.prototype.setComplete = function () {
	this.fileProgressElement.className = "progressContainer blue";
	this.fileProgressElement.childNodes[3].className = "progressBarComplete";
	this.fileProgressElement.childNodes[3].style.width = "";

};
FileProgress.prototype.setError = function () {
	this.fileProgressElement.className = "progressContainer red";
	this.fileProgressElement.childNodes[3].className = "progressBarError";
	this.fileProgressElement.childNodes[3].style.width = "";

};
FileProgress.prototype.setCancelled = function () {
	this.fileProgressElement.className = "progressContainer";
	this.fileProgressElement.childNodes[3].className = "progressBarError";
	this.fileProgressElement.childNodes[3].style.width = "";

};
FileProgress.prototype.setStatus = function (status) {
	this.fileProgressElement.childNodes[2].innerHTML = status;
};

FileProgress.prototype.toggleCancel = function (show, swfuploadInstance) {
	this.fileProgressElement.childNodes[0].style.visibility = show ? "visible" : "hidden";
	if (swfuploadInstance) {
		var fileID = this.fileProgressID;
		this.fileProgressElement.childNodes[0].onclick = function () {
			swfuploadInstance.cancelUpload(fileID);
			return false;
		};
	}
};
