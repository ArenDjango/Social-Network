$('#formlike').on('submit', function(event){
    event.preventDefault();

    $.ajax({
        url : '/photo/{{ photos.id }}/',
        type : 'POST',
        data : {},

        success : function(data){
            
      		console.log('Its working!')
        }
    });
});