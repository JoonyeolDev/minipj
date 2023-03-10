$(document).ready(function () {
  show_wishlist();
});

function show_wishlist() {
  fetch("/wishlist")
    .then((res) => res.json())
    .then((data) => {
      let rows = data["result"];

      $("#espostit1").empty();
      $("#espostit2").empty();
      $("#espostit3").empty();
      $("#espostit4").empty();
      $("#espostit5").empty();
      rows.forEach((a) => {
        let mypostit = a["mypostit"];
        let post_id = a["post_id"];
        let inputGroupSelect01 = a["inputGroupSelect01"];
        let myurl = a["myurl"];
        let temp_html = `<a href="/${post_id}"><div class="es_smalltitle" draggable="true">
            <div class="es_smalltitleimg"><img src="${myurl}" alt src=""></div>
             <span class ="d-inline-block text-truncate" style="max-width: 85px;">
              ${mypostit}
             </span>
           </div>
        </div></a>`;
        if (inputGroupSelect01 == "투두") {
          $("#espostit1").append(temp_html);
        } else if (inputGroupSelect01 == "위시") {
          $("#espostit2").append(temp_html);
        } else if (inputGroupSelect01 == "여행") {
          $("#espostit3").append(temp_html);
        } else if (inputGroupSelect01 == "게임") {
          $("#espostit4").append(temp_html);
        } else {
          $("#espostit5").append(temp_html);
        }
      });

      $("#mywishlist-list").empty();
      rows.forEach((a) => {
        let inputGroupSelect01 = a["inputGroupSelect01"];
        let myoneline = a["myoneline"];
        let floatingTextarea = a["floatingTextarea"];
        let myurl = a["myurl"];
        let mydate = a["mydate"];
        let nickname = a["nickname"];
        let post_id = a["post_id"];

        let temp_html = `<div class="row row-cols-1 g-4" id="">
        <div class="col">
            <div class="card" style="width: 280px;">
                <div class="sh-heater-likebox">
                    <div class="sh-heater-box">
                        <div class="sh-heater">
                            <a class="sh-title" href="/${post_id}">${myoneline}</a>
                        </div>
                        <div class="sh-heater-in">
                            <p class="sh-date">${mydate}</p>
                        </div>
                    </div>
                    <div class="sh-like-box">
                        <div class="sh-like" onclick="like()"></div>
                        <span class="sh-like-count">0</span>
                    </div>
                </div>
                <div>
                    <img src="${myurl}" id="myurl" class="card-img-top" alt="...">
                </div>
                <div class="card-body">
                    <p class="card-text">${floatingTextarea}</p>
                    <div class="sh-username">by.${nickname}</div>
                </div>
                <div class="card-footer">
                    <small class="text-muted">카테고리[ ${inputGroupSelect01} ]</small>
                </div>
            </div>
        </div>
    </div>`;
        $("#mywishlist-list").append(temp_html);
      });
    });
}

//등록버튼 누르면 함수발생
//wishlist_give라는 이름으로 샘플데이터를 담아서 data를 /wishlist에 보냄 -> app.py에 wishlist_give찾기
function save_wishlist() {
  //입력 데이터 읽어 와야함
  //입력데이터 가져와서 변수에 담음
  let inputGroupSelect01 = $("#inputGroupSelect01").val();
  let mypostit = $("#mypostit").val();
  let myoneline = $("#myoneline").val();
  let floatingTextarea = $("#floatingTextarea").val();
  let myurl = $("#myurl").val();
  let mydate = $("#mydate").val();

  let formData = new FormData();
  formData.append("inputGroupSelect01_give", inputGroupSelect01);
  formData.append("mypostit_give", mypostit);
  formData.append("myoneline_give", myoneline);
  formData.append("floatingTextarea_give", floatingTextarea);
  formData.append("myurl_give", myurl);
  formData.append("mydate_give", mydate);

  fetch("/", { method: "POST", body: formData })
    .then((response) => response.json())
    .then((data) => {
      alert(data["msg"]);
      window.location.reload();
    });
}

function save_comment(post_id) {
  let comment = $("#myo_floatingTextarea").val();
  let formData = new FormData();
  formData.append("comment", comment);
  formData.append("post_id", post_id);
  fetch("/create_comment", { method: "POST", body: formData })
    .then((response) => response.json())
    .then((data) => {
      alert(data["msg"]);
      window.location.reload();
    });
}
