$(document).ready(function(){
  // click on button submit
  $("#submit").on('click', function(event){
    // event.preventDefault();
      // send ajax

      var formdata0 = $("#del_apt_form")
      console.log("Without", formdata0)

      var formdata = $("#del_apt_form").serializeArray();
      var data = {};
      
      console.log('Form data', formdata);

      console.log(`id = ${formdata[0].name} || value = ${formdata[0].value}`)

      data[formdata[0].name] = formdata[0].value

      console.log("FORM SERIAL HERE:", data)

      // $(formdata ).each(function(index, obj){
      //     data[obj.name] = obj.value;
      // });
      data=JSON.stringify(data)
      console.log(data)
      $.ajax({
          url: `/api/input_del_appointments`, // url where to submit the request
          type : "DELETE", // type of action POST || GET
          data : data, // post data || get data
          dataType : 'json',
          contentType: "application/json; charset=utf-8",

          success : function(result) {
              // you can see the result from the console
              // tab of the developer tools
              console.log(result);
          },
          error: function(xhr, resp, text) {
              console.log(xhr, resp, text);
          }
      })

  });
});