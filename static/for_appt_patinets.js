pat_table = document.getElementById("#pat_table")
$(document).ready(function(){
  // click on button submit
      // result=""
      $.ajax({
          url: '/api/appointment', // url where to submit the request
          type : "GET", // type of action POST || GET
          success : function(result) {
              // you can see the result from the console
              // tab of the developer tools
              // console.log(result);
              j_data = JSON.stringify(result)
              json_data = JSON.parse(j_data)
              console.log(json_data)

              json_data.forEach((json_object)=> {
                console.log(json_object.id, json_object.name, json_object.checkup_type);
                
              })
              
              if ($("#pat_table tbody").lenght == 0) {
                $("#pat_table").append("<tbody></tbody>")
              }
                json_data.forEach((json_object)=> {
                  $("#pat_table tbody").append(
                  "<tr>" + 
                    `<td>${json_object.id}</td>` + 
                    `<td>${json_object.name}</td>` +
                    `<td>${json_object.checkup_type}</td>` +
                  "</tr>")
                }
              )
          },
          error: function(xhr, resp, text) {
              console.log(xhr, resp, text);
          }
      })
});