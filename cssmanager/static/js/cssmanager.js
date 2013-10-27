$(document).ready(function(){

  function getHexRGBColor(color){
      color = color.replace(/\s/g,"");
      var aRGB = color.match(/^rgb\((\d{1,3}[%]?),(\d{1,3}[%]?),(\d{1,3}[%]?)\)$/i);
      if(aRGB){
         color = '';
         for (var i=1;  i<=3; i++) color += Math.round((aRGB[i][aRGB[i].length-1]=="%"?2.55:1)*parseInt(aRGB[i])).toString(16).replace(/^(.)$/,'0$1');
      }
          else color = color.replace(/^#?([\da-f])([\da-f])([\da-f])$/i, '$1$1$2$2$3$3');
          return color;
  }

  $('.pan').tabSlideOut({							//Класс панели
    		tabHandle: '.handle',						//Класс кнопки
    		pathToTabImage: '/static/images/cssmanager.gif',				//Путь к изображению кнопки
    		imageHeight: '122px',						//Высота кнопки
    		imageWidth: '40px',						//Ширина кнопки
    		tabLocation: 'right',						//Расположение панели top - выдвигается сверху, right - выдвигается справа, bottom - выдвигается снизу, left - выдвигается слева
    		speed: 300,								//Скорость анимации
    		action: 'click',								//Метод показа click - выдвигается по клику на кнопку, hover - выдвигается при наведении курсора
    		topPos: '200px',							//Отступ сверху
    		fixedPosition: true						//Позиционирование блока false - position: absolute, true - position: fixed
    	});


    $('.pan').on('click', 'li', function(event){

        $.ajax({
            url: "/cssmanager/dirscss/",
            data: "dir=" + encodeURIComponent($(this).attr('par')),
            success: function(html){
                $("#listcss").html(html);
                //$(".pan").css("overflow","scroll")
                }
        });
    });



    $('.pan').on('click', 'ul', function() {

        sel=$(this).text();
        file=$(this).attr('par');
        //var html = [ ];
        var stylePropsColor = $(sel).css([ "color", "background-color"]);  //Додавати css властивості з вибором кольору
        var styleProps = $(sel).css(["width", "height"]); //Додавати css властивості
        var str=""
        var DictSel=""
        str=str+"<li par="+file+">..</li><br>"
        try{
        $.each( stylePropsColor, function( prop, value ) {
            str=str+ prop + ": " + "<input class="+prop+" type="+"text"+" sel="+sel+" prop="+prop+" value=#"+getHexRGBColor(value)+"><br>";
            DictSel=DictSel+" ."+prop+",";
        });

        $.each( styleProps, function( prop, value ) {
            str=str+ prop + ": " + "<input class="+prop+" type="+"text"+" sel="+sel+" prop="+prop+" value="+value+"><br>";
        });

        str=str+"<div id='res_message'></div>"
        str=str+"<input id='csssave' sel="+sel+" type='submit' name='save' value='Save'>";
        $("#listcss").html( str );

        $(DictSel.slice(0,-1)).ColorPicker({
        onSubmit: function(hsb, hex, rgb, el) {
		        $(el).val('#'+hex);
		        $(el).ColorPickerHide();
                $($(el).attr('sel')).css($(el).attr('prop'),$(el).val());
	        },
	    onBeforeShow: function () {
		    $(this).ColorPickerSetColor(this.value);
	        }
        })
      }
        catch(err){
            str=str+'Selected selector is missing on this page'
            $("#listcss").html(str);}
    });

    function getcss(){
        var arr=[] ;
        $(".pan input:text").each(function() {
            arr.push($(this).attr('prop')+":"+$(this).val());
        });
        return encodeURIComponent(arr)
    }


    $(".pan").on('click','#csssave',function(){
        $.ajax({
            url: "/cssmanager/submitcss/",
            data: "selector="+$(this).attr('sel')+"&prop="+getcss(),
            success: function(html){
                $("#res_message").html(html);
                }
        });
    });

    $(".pan").on('keyup','input',function(){
        $($(this).attr('sel')).css($(this).attr('prop'),$(this).val());
    });
});