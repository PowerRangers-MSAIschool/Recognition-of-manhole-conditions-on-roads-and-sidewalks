let outputDiv = document.getElementById('text_notification');

window.onload = function(){
    // switchElement1 -> 알림 버튼
    const switchElement1 = document.getElementById('alertToggle');
    // switchElement1 -> 작업시작 버튼
    const switchElement2 = document.getElementById('workToggle');
    
  
    let intervalId;  // setInterval을 관리하기 위한 변수

    // 알림 토글 on 시 사운드 출력 처리
    switchElement1.addEventListener('change', function () {
        if (this.checked) {
            // 스위치가 켜진 경우, 주기적으로 Django View에서 데이터 가져오기
            playAlertAudio();
            intervalId = setInterval(playAlertAudio, 5000);  // 1초마다 실행 (1000ms)
        } else {
            // 스위치가 꺼진 경우, 오디오 중지 및 setInterval 해제
            stopAudio();
            clearInterval(intervalId);
        }
    });
    switchElement2.addEventListener('change', function () {
        if (this.checked) {
            // 스위치가 켜진 경우, 주기적으로 Django View에서 데이터 가져오기
            // Promise를 반환하는 displaystatus 함수 호출
            displaystatus();
            intervalId = setInterval(displaystatus, 1000);
            // outputDiv.innerHTML = "작업버튼(ON)";
        } else {
            clearInterval(intervalId);
        }
    });
}
// 주기적으로 Django View에서 데이터 가져와 처리하는 함수
function playAlertAudio() {
    fetch('send_status', {
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // JavaScript에서 데이터 처리 및 오디오 재생
        if (data.sound == 'True') {
            playAudio();
        }
    });
}

function displaystatus() {
    fetch('send_status', {
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => { // manhole_closed, hole, person, sound
        // 가져온 딕셔너리의 조건대로 텍스트 출력
        outputDiv.innerHTML = data.person
        if (data.person == 'True'){
            outputDiv.innerHTML = "멘홀 작업 중 보행자가 감지되었습니다."
        }
        if (data.manhole_hole == 'False'){
            outputDiv.innerHTML = "멘홀이 닫혀 있습니다."
        }
    });
}

// 오디오 재생 함수
function playAudio() {
    // 실제로 사용할 오디오 파일 경로를 설정
    const audioPath = '/static/audio/alert.mp3';  // 예시 경로, 실제 경로에 맞게 수정

    // 오디오 엘리먼트 생성 및 재생
    const audio = new Audio(audioPath);
    audio.play();
}

// 오디오 중지 함수
function stopAudio() {
    // 모든 오디오 엘리먼트 중지
    const allAudioElements = document.querySelectorAll('audio');
    allAudioElements.forEach(audio => audio.pause());
}

