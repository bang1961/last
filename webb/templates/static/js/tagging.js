$(document).ready(function () {
    console.log('successsss')
    $('[name^=tagging]').each(function () {
        let pk = $(this).attr('id');
        $.ajax({
            type: "POST",
            url: "{% url ' src:like_ready' %}",
            data: {
                'pk': pk,
                
                'csrfmiddlewaretoken': '{{ csrf_token }}'

            },
            dataType: "json",
            success: function(response) {
                
                $('.like').attr('disabled', true);
                $('.dislike').attr('disabled', true);
                $('.tagging_reset').attr('disabled', true);

                $('.pb'+pk).css('width', (response.Tag_count/{{ all_member }})*100+'%');
                $('.pb'+pk+' span').text(response.Tag_count);
                
                $('#'+pk).text(response.message+' ').attr('class', (response.message!=="Cancel ")?'like btn btn-success glyphicon glyphicon-thumbs-up':'like btn btn-danger glyphicon glyphicon-thumbs-down');
                $('#'+pk).text(' ' + response.message);

                if (response.message == "Cancel "){
                    $('.like').attr('disabled', true);
                    $('.dislike').attr('disabled', true);
                    $('.tagging_reset').attr('disabled', false);
                }
                else{
                    $('.like').attr('disabled', false);
                    $('.dislike').attr('disabled', false);
                    $('.tagging_reset').attr('disabled', true);
                }
                if(dday>0){
                    $('#'+pk).attr('class', (response.message !== "Cancel ") ? 'like btn btn-success glyphicon glyphicon-thumbs-up' : 'like btn btn-danger glyphicon glyphicon-thumbs-down');
                }
                else{
                    $('#'+pk).attr('class', (response.message !== "Cancel ") ? 'like btn btn-success glyphicon glyphicon-thumbs-up disabled' : 'like btn btn-danger glyphicon glyphicon-thumbs-down disabled').attr('disabled', 'disabled');
                }
            },
            error: function(request, status, error) {
                console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            }
        });
        
    })
});

{% comment %} 버튼을 눌렀을 때 Like {% endcomment %}
{% if user.is_authenticated %}
$('.like').click(function() {
    let pk = $(this).attr('id');
    $.ajax({
        type: "POST",
        url: "{% url ' src:like' %}",
        data: {
            'pk': pk,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        dataType: "json",
        success: function(response) {
            $('.like').attr('disabled', true);
            $('.dislike').attr('disabled', true);
            $('.tagging_reset').attr('disabled', true);

            $('.pb'+pk).css('width', (response.Tag_count/{{ all_member }})*100+'%');
            $('.pb'+pk+' span').text(response.Tag_count);

            {% comment %} $('#'+pk).text(response.message+' ').attr('class', (response.message!=="Cancel ")?'like btn btn-success glyphicon glyphicon-thumbs-up':'like btn btn-danger glyphicon glyphicon-thumbs-down'); {% endcomment %}
            
            if (response.message == "Cancel "){
                $('.like').attr('disabled', true);
                $('.dislike').attr('disabled', true);
                $('.tagging_reset').attr('disabled', false);

            } else {
                $('.like').attr('disabled', false);
                $('.dislike').attr('disabled', false);
                $('.tagging_reset').attr('disabled', true);
            }
        },
        error: function(request, status, error) {
            alert("로그인이 필요합니다.");
            console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        }
    });
})

{% endif %}

{% comment %} DisLike데이터 전달 후 else {% endcomment %}

$(document).ready(function () {
$('[name^=tagging1]').each(function () {
    let pk = $(this).attr('id');
    $.ajax({
        type: "POST",
        url: "{% url ' src:dislike_ready' %}",
        data: {
            'pk': pk,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        dataType: "json",
        success: function(response) {
            $('.like').attr('disabled', true);
            $('.dislike').attr('disabled', true);
            $('.tagging_reset').attr('disabled', true);

            $('.pb1'+pk).css('width', (response.Tags_default/{{ all_member }})*100+'%');
            $('.pb1'+pk+' span').text(response.Tags_default);
            
            {% comment %} $('.dislike').text(response.message1+' ').attr('class', (response.message1!=="Cancel ")?'dislike btn btn-danger glyphicon glyphicon-thumbs-down':'dislike btn btn-success glyphicon glyphicon-thumbs-up');
            $('.dislike').text(' ' + response.message1); {% endcomment %}

            if (response.message1 == "Cancel "){
                $('.like').attr('disabled', true);
                $('.dislike').attr('disabled', true);
                $('.tagging_reset').attr('disabled', false);

            } 
            else{
                $('.like').attr('disabled', false);
                $('.dislike').attr('disabled', false);
                $('.tagging_reset').attr('disabled', true);
            }
            if(dday>0){
                $('.dislike').attr('class', (response.message1 !== "Cancel ") ? 'dislike btn btn-danger glyphicon glyphicon-thumbs-down' : 'dislike btn btn-success glyphicon glyphicon-thumbs-up');
            }
            else{
                $('.dislike').attr('class', (response.message1 !== "Cancel ") ? 'dislike btn btn-danger glyphicon glyphicon-thumbs-down disabled' : 'dislike btn btn-success glyphicon glyphicon-thumbs-up disabled').attr('disabled', 'disabled');
            }
        },
        error: function(request, status, error) {
            console.log("code:" + request.status + "\n" + "message1:" + request.responseText + "\n" + "error:" + error);
        }
    });
    
})
});

{% comment %} 버튼을 눌렀을 때 DisLike     {% endcomment %}



{% if user.is_authenticated %}
$('.dislike').click(function() {
let pk = $(this).attr('id');
$.ajax({
    type: "POST",
    url: "{% url ' src:dislike' %}",
    data: {
        'pk': pk,
        'csrfmiddlewaretoken': '{{ csrf_token }}'
    },
    dataType: "json",
    success: function(response) {
        $('.like').attr('disabled', true);
        $('.dislike').attr('disabled', true);
        $('.tagging_reset').attr('disabled', true);
        
        $('.pb1'+pk).css('width', (response.Tags_default/{{ all_member }})*100+'%');
        $('.pb1'+pk+' span').text(response.Tags_default);
        
        {% comment %} $('.dislike').text(response.message1+' ').attr('class', (response.message1!=="Cancel ")?'dislike btn btn-danger glyphicon glyphicon-thumbs-down':'dislike btn btn-success glyphicon glyphicon-thumbs-up'); {% endcomment %}
        if (response.message1 == "Cancel "){
            $('.like').attr('disabled', true);
            $('.dislike').attr('disabled', true);
            $('.tagging_reset').attr('disabled', false);
        } 
        else{
            $('.like').attr('disabled', false);
            $('.dislike').attr('disabled', false);
            $('.tagging_reset').attr('disabled', true);
        }
    },
    error: function(request, status, error) {
        alert("로그인이 필요합니다.");
        console.log("code:" + request.status + "\n" + "message1:" + request.responseText + "\n" + "error:" + error);
    }
});
})

{% endif %}

{% if user.is_authenticated %}
$('.tagging_reset').click(function() {
let pk = $(this).attr('id');
$.ajax({
    type: "POST",
    url: "{% url ' src:tagging_reset_like' %}",
    data: {
        'pk': pk,
        'csrfmiddlewaretoken': '{{ csrf_token }}'
    },
    dataType: "json",
    success: function(response) {
        
        $('.pb'+pk).css('width', (response.Tag_count/{{ all_member }})*100+'%');
        $('.pb'+pk+' span').text(response.Tag_count);
        $('.like').attr('disabled', false);
        $('.dislike').attr('disabled', false);
        $('.tagging_reset').attr('disabled', true);


        
    },
    error: function(request, status, error) {
        alert("로그인이 필요합니다.");
        console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
    }
});
})

{% endif %}

{% if user.is_authenticated %}
$('.tagging_reset').click(function() {
let pk = $(this).attr('id');
$.ajax({
    type: "POST",
    url: "{% url ' src:tagging_reset_dislike' %}",
    data: {
        'pk': pk,
        'csrfmiddlewaretoken': '{{ csrf_token }}'
    },
    dataType: "json",
    success: function(response) {
        $('.pb1'+pk).css('width', (response.Tags_default/{{ all_member }})*100+'%');
        $('.pb1'+pk+' span').text(response.Tags_default);
        
    },
    error: function(request, status, error) {
        alert("로그인이 필요합니다.1");
        console.log("code:" + request.status + "\n" + "message1:" + request.responseText + "\n" + "error:" + error);
    }
});
})

{% endif %}



$(document).ready(function () {

var tmp = parseInt($("#test_obj").css('top'));

$(window).scroll(function () {
    var scrollTop = $(window).scrollTop();
    var obj_position = scrollTop + tmp + "px";

    $("#test_obj").stop().animate({
        "top": obj_position
    }, 500);
    
}).scroll();
});

$(document).ready(function() {
 $('ul.tabs li').click(function(){
    var tab_id = $(this).attr('data-tab');

    $('ul.tabs li').removeClass('current');
    $('.tab-content').removeClass('current');
 
    $(this).addClass('current');
    $("#"+tab_id).addClass('current');
  })

});

$(document).ready(function(){ 
//이벤트 발생 전 선택된 값 
var preValue = $("input[name='radio_like']:checked").val(); 
//클릭 이벤트 발생 
    $("input[name='radio_like']").click(function()
    { 
        if(confirm("변경하시겠습니까?") == false) {
             //체크 해제 
             $(this).prop('checked', false); 
             //이전 라디오버튼 체크 
             $("input[name='radio_like']:radio[value='" + preValue + "']").prop('checked', true); 
             return; 
        } 
        preValue = $(this).val(); 
    }); 
});