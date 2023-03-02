function myFunction() {
    var x = document.getElementById("password-field");
    var y = document.querySelector(".toggle-password");
    if (x.type === "password") {
      x.type = "text";
      y.classList.remove("fa-eye")
      y.classList.add("fa-eye-slash")
    } else {
      x.type = "password";
      y.classList.remove("fa-eye-slash")
      y.classList.add("fa-eye")
    }
  }
  function myFunction2() {
    var x = document.getElementById("conf-password-field");
    var y = document.querySelector(".toggle-password-conf");
    if (x.type === "password") {
      x.type = "text";
      y.classList.remove("fa-eye")
      y.classList.add("fa-eye-slash")
    } else {
      x.type = "password";
      y.classList.remove("fa-eye-slash")
      y.classList.add("fa-eye")
    }
  }
  const signInUser = () => {
    //  e.preventDefault()
    // console.log('clicked');
    const data = {
        //name: document.querySelector("#name").value,
        email: document.querySelector("#email").value,
        password: document.querySelector("#password-field").value,
    }
    console.log(data)
   //       });
   axios.post('/users/login', data)
      .then(function(response) {
          if (response.status == 200) {
              
              window.location.href = '/posts'
          }
          console.log(response.data.token)
      })
      .catch(function(error) {
          if (error.response) {
              //alert(error.response.data.error);
              swal(error.response.data.error, "Please try again!", "error");
          }
      });
}
  const createUser = () => {
      //  e.preventDefault()
      // console.log('clicked');
      const data = {
          name: document.querySelector("#name").value,
          email: document.querySelector("#email").value,
          password: document.querySelector("#password-field").value,
      }
      axios.post('/users/register', data)
          .then(function(response) {
              if (response.status == 200) {
                  //alert(response.data.msg);
                  window.location.href = '/users/login'
              }
          })
          .catch(function(error) {
              if (error.response) {
                  swal(error.response.data.error, "Please try again!", "error");
              }
          });
  }
  const uploadImage = async(files) => {
      const input = document.querySelector('.drop-zone__input');
      const data = new FormData();
      if (!input.files[0]) {
        swal("Please upload an image","error")
          return
      }
      data.append('file', input.files[0]);
      data.append('upload_preset', cloudinary.preset);
      data.append('public_id', `posts/${user.id}${Math.floor(Math.random() * 1000000000)}`);
      data.append('api_key', cloudinary.apiKey);
      const res = await fetch(`https://api.cloudinary.com/v1_1/${cloudinary.name}/image/upload`, {
          method: 'POST',
          body: data
      });
  
      const file = await res.json();
      
      console.log(file.secure_url);
      return file.secure_url;
  }
  const createPost = async() => {
      const image = await uploadImage()
      const data = {
          title: document.querySelector("#title").value,
          author: user.id,
          content: document.querySelector("#content").value,
          image,
          tag: document.querySelector('#selectInput').value,
          createdAt: new Date(),
      }
      axios.post('/posts/createPost', data)
          .then(function(response) {
              if (response.status == 200) {
                  window.location.href = `/posts/${response.data.id}`
              }
          })
          .catch(function(error) {
              if (error.response) {
                swal(error.response.data.error, "Please try again!", "error");
                  
              }
          });
  }