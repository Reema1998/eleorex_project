// $('#mainRightNav').addClass('disabled');
var resultArray = JSON.parse(queryArray);

//alert(JSON.stringify(queryArray));
var arrayLen = resultArray.DATA.length;
var user_id = document.getElementById("recordbtn").getAttribute("data-userid");
var attendDate = document.getElementById("recordbtn").getAttribute("data-attenddate");
var totalQtn = totalquestion;
var qtnstart = totalquestion - arrayLen;
Qcount = arrayLen;
QarrCount = qtnstart;
arrCount = 0;
var filearray = 0;
var QtnCount = 0;
var idCount = QarrCount+1;
var preId = idCount-1;
var video_name_last = 'Not Found';
var alert_in_progress = 0;


$('.questions').html(resultArray.DATA[0][0]);
$('.timeOut').html(resultArray.DATA[0][1]);
$('.count').html(QarrCount+1);
$('.countdown').html(resultArray.DATA[0][1]);

var doUpdate = function() {
  $('.countdown').each(function() {
    var count = parseInt($(this).html());
    if (count !== 0) {
      $(this).html(count - 1);
    }else{

      clearInterval(interval);
        clearTimeout(setTimeclear);
        $('#sideQnBtns_'+idCount+'').addClass('completed');
        $('#sideQnBtns_'+idCount+'').addClass('disabled');
        $('#stop').prop('disabled', true);
        console.log("Stop rec..."+Qcount);
      
			tagRecorder.stopVideo();
			
			//enabling the stop button, disabling the record button
			stopbtn.disabled = true;
    
    }
  });
};


  


  

PipeSDK.onRecordersInserted = function(){
  //getting the reference to our recorder objects	
  
  $('piperecorder#first-recorder').attr('pipe-mrt',resultArray.DATA[0][1]);

	tagRecorder =  PipeSDK.getRecorderById('first-recorder');
	//getting the reference to the custom buttons
	recbtn = document.getElementById("recordbtn");
	stopbtn = document.getElementById("stopbtn");
	//savebtn = document.getElementById("savebtn");
  //Calling control API methods when the desktop event function onReadyToRecord() is triggered

  

	tagRecorder.onReadyToRecord = function(id, type){
		var args = Array.prototype.slice.call(arguments);
		__log("onReadyToRecord("+args.join(', ')+")");
		recbtn.disabled = false;
		
		recbtn.onclick = function (){
      interval = setInterval(doUpdate, 999);
      var clockTime = resultArray.DATA[arrCount][1] * 1000;
			tagRecorder.record();
			recbtn.disabled = true;
      stopbtn.disabled = false;
      
      setTimeclear = setTimeout( function(){
        document.VideoRecorder.stopVideo();
     },clockTime);
    }

		
		stopbtn.onclick = function (){
      //calling the control API method
        clearInterval(interval);
        clearTimeout(setTimeclear);
        $('#sideQnBtns_'+idCount+'').addClass('completed');
        $('#sideQnBtns_'+idCount+'').addClass('disabled');
        $('#stop').prop('disabled', true);
        console.log("Stop rec..."+Qcount);
      
			tagRecorder.stopVideo();
			
			//enabling the stop button, disabling the record button
      stopbtn.disabled = true;
      
		}
		// savebtn.onclick = function (){
		// 	//calling the control API method
		// 	tagRecorder.save();
			
		// 	//disabling the save button
		// 	//savebtn.disabled = true;
		// }
		
	}
	//========================== Events API for first Recorder ===============================
	
	//DESKTOP EVENTS API

tagRecorder.userHasCamMic = function(id,camNr, micNr){
  var cam = camNr;
  var microphone = micNr;
  var err = '';
  if (!cam){
    err = err+' please connect cam!!';
  }else if(!microphone){
    err = err +'please connect microphone!!';
  }
  if(err.length){
    alert(err);
    location.reload();
    $('#recordbtn').prop('disabled', true);
    $('#stopbtn').prop('disabled', true);
    return false;
  }
  else{
    // alert('please click Start interview to start your interview!')
    $('#recordbtn').prop('disabled', false);
  }
  var args = Array.prototype.slice.call(arguments);
  __log("userHasCamMic("+args.join(', ')+")");
}
	
	tagRecorder.btRecordPressed = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("btRecordPressed("+args.join(', ')+")");
	}
	
	tagRecorder.btStopRecordingPressed = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("btStopRecordingPressed("+args.join(', ')+")");
	}
	
	
	tagRecorder.onUploadDone = function(recorderId, streamName, streamDuration, audioCodec, videoCodec, fileType, audioOnly, location){
		var args = Array.prototype.slice.call(arguments);
		__log("onUploadDone("+args.join(', ')+")");
		
    //enabling record, play and save buttons
    tagRecorder.save();
		recbtn.disabled = false;
		// playbtn.disabled = false;
		// savebtn.disabled = false;
	}
	
	tagRecorder.onCamAccess = function(id, allowed){
		var args = Array.prototype.slice.call(arguments);
		__log("onCamAccess("+args.join(', ')+")");
	}
	
	tagRecorder.onPlaybackComplete = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("onPlaybackComplete("+args.join(', ')+")");
		
		//enabling play button, disabling pause button
		// playbtn.disabled = false;
		// pausebtn.disabled = true;
	}
	
	tagRecorder.onRecordingStarted = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("onRecordingStarted("+args.join(', ')+")");
	}
	
	tagRecorder.onConnectionClosed = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("onConnectionClosed("+args.join(', ')+")");
	}
	
	tagRecorder.onConnectionStatus = function(id, status){
		var args = Array.prototype.slice.call(arguments);
		__log("onConnectionStatus("+args.join(', ')+")");
	}
	
	tagRecorder.onMicActivityLevel = function(id, level){
		var args = Array.prototype.slice.call(arguments);
		//__log("onMicActivityLevel("+args.join(', ')+")");
	}
	
	tagRecorder.onFPSChange = function(id, fps){
		var args = Array.prototype.slice.call(arguments);
		//__log("onFPSChange("+args.join(', ')+")");
	}
  

	tagRecorder.onSaveOk = function(recorderId, streamName, streamDuration, cameraName, micName, audioCodec, videoCodec, filetype, videoId, audioOnly, location){
		var args = Array.prototype.slice.call(arguments);
    __log("onSaveOk("+args.join(', ')+")");
    //////////////////////////////////////////////////////////////////////////////////////////////

        var fileName = resultArray.DATA[filearray][2];
        var location = location;
        var video_name = streamName;
        var videoId = videoId;
        if (practice_flag === "False") {
          var custom_url = '/interviewee/interview/'.concat(interviewId,'/');
        }
        else {
          var custom_url = '/interviewee/interview/practice/';
        }
        $.ajax({
            url : custom_url,
            data: {'candidate_ID':user_id, 'interview_ID': interviewId, 'question_ID':fileName, 'location':location, 'video_name':video_name, 'videoId':videoId},
            headers: {'X-CSRFToken':getCookie('csrftoken')
                ,'sessionid':getCookie('sessionid')
                },
            success : function(data){
              console.log(data);
              if(data != 0){
                console.log('success!!!');
                if(Qcount > 1 ){
                  Qcount--;
                  arrCount++;
                  QarrCount++;
                  var slNo = QarrCount+1;
                  alert('Video answer completed');
                  idCount++;
                  preId = idCount - 1;
                $('.qnMainContainer').css("display","none");
                $('.qnIntroOverlay').show();
                $('.questions').html(resultArray.DATA[arrCount][0]);
                  $('.timeOut').html(resultArray.DATA[arrCount][1]);
                  $('.count').html(slNo);
                  $('.countdown').html(resultArray.DATA[arrCount][1]);
                }else{
                  alert('Thanks for Interview.');
                  window.location.reload();
                }

              QtnCount++;
                filearray++;
              console.log(QtnCount);
              if(QtnCount == arrayLen){
                updateInterviewStatus(QtnCount);
              }
            }else{
              alert('Question not uploaded, please try again!!');
              $('.qnMainContainer').css("display","none");
              $('.qnIntroOverlay').show();
              $('.questions').html(resultArray.DATA[arrCount][0]);
                $('.timeOut').html(resultArray.DATA[arrCount][1]);
                $('.count').html(slNo);
                $('.countdown').html(resultArray.DATA[arrCount][1]);
                $('#capture-button').prop('disabled', false);
              $('#stop').prop('disabled', false);
            }
            },
            error:function(data,exception){
              alert('Something Went Wrong, try again!!');
              $('.qnMainContainer').css("display","none");
            $('.qnIntroOverlay').show();
            $('.questions').html(resultArray.DATA[arrCount][0]);
              $('.timeOut').html(resultArray.DATA[arrCount][1]);
              $('.count').html(slNo);
              $('.countdown').html(resultArray.DATA[arrCount][1]);
              $('#capture-button').prop('disabled', false);
            $('#stop').prop('disabled', false);
            }
        });

    /////////////////////////////////////////////////////////////////////////////////////////////////
	}
	
	tagRecorder.onFlashReady = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("onFlashReady("+args.join(', ')+")");
	}
	
	//DESKTOP UPLOAD EVENTS API
	tagRecorder.onDesktopVideoUploadStarted = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("onDesktopVideoUploadStarted("+args.join(', ')+")");
	}
	
	tagRecorder.onDesktopVideoUploadSuccess = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("onDesktopVideoUploadSuccess("+args.join(', ')+")");
	}
	
	tagRecorder.onDesktopVideoUploadFailed = function(id){
		var args = Array.prototype.slice.call(arguments);
		__log("onDesktopVideoUploadFailed("+args.join(', ')+")");
	}
			
		
	//MOBILE EVENTS API
	tagRecorder.onVideoUploadStarted = function(recorderId, filename, filetype, audioOnly){
		var args = Array.prototype.slice.call(arguments);
		__log("onVideoUploadStarted("+args.join(', ')+")");
	}
	
	tagRecorder.onVideoUploadSuccess = function(recorderId, filename, filetype, videoId, audioOnly, location){
		var args = Array.prototype.slice.call(arguments);
    __log("onVideoUploadSuccess("+args.join(', ')+")");
    
    //////////////////////////////////////////////////////////////////////////////////////////////

    var fileName = resultArray.DATA[filearray][2];
    var location = location;
    var video_name = filename;
    var videoId = videoId;
    if (practice_flag === "False") {
      var custom_url = '/interviewee/interview/'.concat(interviewId,'/');
    }
    else {
      var custom_url = '/interviewee/interview/practice/';
    }
    $.ajax({
        url : custom_url,
        data: {'candidate_ID':user_id, 'interview_ID': interviewId, 'question_ID':fileName, 'location':location, 'video_name':video_name, 'videoId':videoId},
        headers: {'X-CSRFToken':getCookie('csrftoken')
            ,'sessionid':getCookie('sessionid')
            },
        success : function(data){
          console.log(data);
          if(data != 0){
            console.log('success!!!');
            if(Qcount > 1 ){
              Qcount--;
              arrCount++;
              QarrCount++;
              var slNo = QarrCount+1;
              alert('Video answer completed');
              idCount++;
              preId = idCount - 1;
            $('.qnMainContainer').css("display","none");
            $('.qnIntroOverlay').show();
            $('.questions').html(resultArray.DATA[arrCount][0]);
              $('.timeOut').html(resultArray.DATA[arrCount][1]);
              $('.count').html(slNo);
              $('.countdown').html(resultArray.DATA[arrCount][1]);
            }else{
              alert('Thanks for Interview.');
              window.location.reload();
            }

          QtnCount++;
            filearray++;
          console.log(QtnCount);
          if(QtnCount == arrayLen){
            updateInterviewStatus(QtnCount);
          }
        }else{
          alert('Question not uploaded, please try again!!');
          $('.qnMainContainer').css("display","none");
          $('.qnIntroOverlay').show();
          $('.questions').html(resultArray.DATA[arrCount][0]);
            $('.timeOut').html(resultArray.DATA[arrCount][1]);
            $('.count').html(slNo);
            $('.countdown').html(resultArray.DATA[arrCount][1]);
            $('#capture-button').prop('disabled', false);
          $('#stop').prop('disabled', false);
        }
        },
        error:function(data,exception){
          alert('Something Went Wrong, try again!!');
          $('.qnMainContainer').css("display","none");
        $('.qnIntroOverlay').show();
        $('.questions').html(resultArray.DATA[arrCount][0]);
          $('.timeOut').html(resultArray.DATA[arrCount][1]);
          $('.count').html(slNo);
          $('.countdown').html(resultArray.DATA[arrCount][1]);
          $('#capture-button').prop('disabled', false);
        $('#stop').prop('disabled', false);
        }
    });

/////////////////////////////////////////////////////////////////////////////////////////////////


	}
	
	tagRecorder.onVideoUploadProgress = function(recorderId, percent){
		var args = Array.prototype.slice.call(arguments);
		__log("onVideoUploadProgress("+args.join(', ')+")");
	}
	
	tagRecorder.onVideoUploadFailed = function(id, error){
		var args = Array.prototype.slice.call(arguments);
		__log("onVideoUploadFailed("+args.join(', ')+")");
	}				
}

//Logger
function __log(e, data) {
	//log.innerHTML += "\n" + e + " " + (data || '');
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
}
});
