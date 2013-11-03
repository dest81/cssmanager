$(document).ready(function() {

    /*Ф-я конвертування кольору HEX to RGB*/
    function getHexRGBColor( color ) {
        color = color.replace(/\s/g, "");
        var aRGB = color.match(/^rgb\((\d{1,3}[%]?),(\d{1,3}[%]?),(\d{1,3}[%]?)\)$/i);
        if(aRGB){
            color = '';
            for (var i=1; i<=3; i++) color += Math.round((aRGB[i][aRGB[i].length-1]=="%"?2.55:1) * parseInt(aRGB[i])).toString(16).replace(/^(.)$/, '0$1');
        } else
            color = color.replace(/^#?([\da-f])([\da-f])([\da-f])$/i, '$1$1$2$2$3$3');
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

    // Вибір директорії файл-бравзера
    $('.pan').on( 'click', '.dir', function( event ) {
        $.ajax({
            url: "/cssmanager/dirscss/",
            data: "dir=" + encodeURIComponent($(this).attr('par')),
            success: function( html ){
                $("#listcss").html( html );
            }
        });
    });

    // Вибір файлу файл-бравзера
    $('.pan').on( 'click', '.file', function( event ) {
        $.ajax({
            url: "/cssmanager/dirscss/",
            data: "dir=" + encodeURIComponent($(this).attr('par')),
            success: function( data ){
                var items = [];
                items.push( "<li class='dir' par=" + data.back + ">..</li>" );
                $.each( data.selectors, function( key, val ) {
                    if($(val).get() != ''){
                        items.push( "<ul par=" + data.pathpar + ">" + val + "</ul>" );
                    }
                });
                $("#listcss").html( items );
            }
        });
    });


    // Вибір селектору
    $('.pan').on( 'click', 'ul', function() {
        sel = $(this).text();
        file = $(this).attr('par');
        //var html = [ ];
        // Сюда можна додавати css властивості з вибором кольору
        var stylePropsColor = $(sel).css(["color", "background-color"]);
        // Сюда можна додавати css властивості
        var styleProps = $(sel).css(["width", "height"]);
        var str = "";
        var DictSel = "";
        str = str + "<li class='file' par=" + file + ">..</li><br>";

        try {
            $.each(stylePropsColor, function(prop, value) {
                str = str + prop + ": " + "<input class=" + prop + " type='text' sel=" + sel + " prop=" + prop + " value=#" + getHexRGBColor(value) + "><br>";
                DictSel = DictSel + " ." + prop + ",";
            });

            $.each( styleProps, function( prop, value ) {
                str=str + prop + ": " + "<input class=" + prop + " type='text' sel=" + sel + " prop=" + prop + " value=" + value + "><br>";
            });

            str = str + "<div id='res_message'></div>";  // Повідомлення
            str = str + "<input id='csssave' sel="+sel+" type='submit' name='save' value='Save'>";
            $("#listcss").html(str);

            $(DictSel.slice(0,-1)).ColorPicker({  //  Показує окно вибору кольору
                onSubmit: function(hsb, hex, rgb, el) {
		            $(el).val('#'+hex);
		            $(el).ColorPickerHide();
                    $($(el).attr('sel')).css($(el).attr('prop'),$(el).val());
	            },
	            onBeforeShow: function () {
		            $(this).ColorPickerSetColor(this.value);
	            }
            })

        } catch( err ) {        // Якщо вибраний селектор відсутній на поточній сторінці
            str = str + 'Selected selector is missing on this page';
            $("#listcss").html(str);
        }
    });

    function getcss() {     //  всі властивості  з форми повертає массивом
        var arr=[] ;
        $(".pan input:text").each(function() {
            arr.push( $(this).attr('prop') + ":" + $(this).val() );
        });
        return encodeURIComponent(arr);
    }

    $(".pan").on( 'click', '#csssave', function() {    // передача властивосте з форми на сервер
        $.ajax({
            url: "/cssmanager/submitcss/",
            data: "selector=" + $(this).attr('sel') + "&prop=" + getcss(),
            success: function( html ){
                $("#res_message").html( html );       // Повідомлення
            }
        });
    });

    $(".pan").on( 'keyup', 'input', function() {             //  в реальному часі міняє властивості
        $($(this).attr('sel')).css( $(this).attr('prop'), $(this).val() );
    });

});