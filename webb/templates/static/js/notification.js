// 브라우저 지원 여부 체크
if (!("Notification" in window)) {
    alert("데스크톱 알림을 지원하지 않는 브라우저입니다.");
}
// 데스크탑 알림 권한 요청
Notification.requestPermission(function (result) {
    // 권한 거절
    if(result == 'denied') {
        alert('알림을 차단하셨습니다.\n브라우저의 사이트 설정에서 변경하실 수 있습니다.');
        return false;
    }
    else if(result == 'granted') {
        console.log('알림을 허용 하셨습니다.' + result);
    }
});
