$(document).ready(function() {
    var reviews = [];
    var currentPage=1;
    var reviewsPerPage = 5;
    var totalReviews = 0; // Total number of reviews
    var totalPages = 0;

    // Function to load all reviews from Flask
    function loadReviews() {
      $.ajax({
        url: '/review/loadcontent',
        type: 'GET',
        success: function(response) {
            totalReviews = response.length;
            totalPages = Math.ceil(totalReviews / reviewsPerPage);
            console.log(totalPages)
          reviews = response;
          showReviews(currentPage);
          // Show the first page of reviews
        },
        error: function(xhr, status, error) {
          console.log('Error:', error);
        }
      });
    }

    // Function to show reviews based on current page
    function showReviews() {
      
      var startIndex = (currentPage - 1) * reviewsPerPage;
      var endIndex = startIndex + reviewsPerPage;
      var displayedReviews = reviews.slice(startIndex, endIndex);

      $('.section').each(function(index) {
        var section = $(this);
        var review = displayedReviews[index];
        section.hide();

        if (review) {
          section.show();
          section.find('.name').text(review.user_name);
          section.find('.timestamp').text(review.timestamp);
          section.find('.paragraph').text(review.paragraph);
        } 
      });
      updateButtons(); 
    }
    function updateButtons() {
      if (currentPage === 1) {
        $('#back').prop('disabled', true);
      } else {
        $('#back').prop('disabled', false);
      }
  
      if (currentPage === totalPages) {
        $('#next').prop('disabled', true);
      } else {
        $('#next').prop('disabled', false);
      }
    }
  
    $('#next').click(function() {
        if (currentPage < totalPages) {
          currentPage++;
          showReviews();
        }
      });
    
      // Function to handle the back button click
      $('#back').click(function() {
        if (currentPage > 1) {
          currentPage--;
          showReviews();
         
        }
      });

    loadReviews(); // Call the loadReviews function when the page loads


    // $('#submitBtn').click(function() {
    //     var review = $('#reviewInput').val();
        
    //     $.ajax({
    //         type: 'POST',
    //         url: '/reviews',
    //         data: {review: review},
    //         success: function(response) {
    //             alert(response.message);
    //             $('#reviewInput').val('');
    //             currentPage = 1;
    //             loadReviews();
    //         },
    //         error: function(xhr, status, error) {
    //             console.log(error);
    //         }
    //     });
    // });
   
        $('#submit').click(function() {
          var review = $('#reviewcomment').val();
          // Replace with the actual username
      

        if (review!==""){
          // Create the review object
          var reviewData = {
            review: review,
            
          };
      
          // Send the review data to the server
          $.ajax({
            url: '/review/submit_review',
            method: 'POST',
            data: reviewData,
            success: function(response) {
                alert(response.message);
                $('#reviewcomment').val('');
              // Handle the success response if needed
              console.log('Review submitted successfully!');
            },
            error: function(error) {
              // Handle the error response if needed
              console.log('Error submitting review:', error);
            }
          });
        }else {
          alert("Please fill the feedback section.");
        }
      
        });
      
      
  });