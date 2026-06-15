//video
let videoBtn= document.querySelectorAll('.vid-btn')

videoBtn.forEach(bttn =>{
    bttn.addEventListener('click', ()=>{
        document.querySelector('.controls .active').classList.remove('active');
        bttn.classList.add('active');
        let src = bttn.getAttribute('data-src');
        document.querySelector('#video-slider').src =src;
    });
});


// slider for review section 
var swiper = new Swiper(".review-slider", {
    spaceBetween:20,
    loop:true,
    autoplay:{
        delay:2500,
        disableOnInteraction: false,
    },
    breakpoints:{
        640:{
            slidesPerView:1,
        },
        768:{
            slidesPeriVew:2,
        },
        1024:{
            slidesPerView:3,
        },
    },
});




/* now when the btn is clicked the no of times the btn is clicked, each time stored in 'updateBtns'
and loop will continue as many times as the btn is clicked  */
var updateBtns= document.getElementsByClassName('update-cart')
 
for(var i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId=this.dataset.product
        var action=this.dataset.action
        console.log('productId:',productId,'action:',action),

        /* for checking the user is authenticated or not, user value is given in layout.html file*/
        console.log('USER:', user)
        if (user== 'AnonymousUser'){     /* in js it is defined that when user is not logged in then the value of user will be AnonymousUser */
            addCookieItem(productId, action)
        }
        else{
            updateUserOrder(productId,action)
        }
    })
}
function addCookieItem(productId, action){
    console.log('Not logged in')

    if (action == 'add'){
        if(cart[productId] == undefined){
            cart[productId]={'quantity':1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }
    if (action =='remove'){
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <=0 ){
            console.log(' Item should be deleted ')
            delete cart[productId];
        }
    }

    console.log('Cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}
 
function updateUserOrder(productId,action){
    console.log('User is logged in, sending data..')

    /* now we use fetch api to send a post request */
    /*this is the url and view where we want to send the data to*/

    var url = '/update_item/' 

    fetch(url,{
        method:'POST',
        /* this sectiion defines what kind of data we are going to send back  */
        headers:{                   
            'content-Type':'application/json',
            'X-CSRFToken':csrftoken,

        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((response) =>{
        return response.json() 
    })
    /* we are consolling out data  which is what our view is sending in back to the template*/
    .then((data) =>{ 
        console.log(data)  
        location.reload()
    })
}




