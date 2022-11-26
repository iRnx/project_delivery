const changeThemeBtn = document.querySelector("#change-theme");

changeThemeBtn.addEventListener('change', function(){

    document.body.classList.toggle('dark')

    if(document.body.classList.contains('dark')){
        localStorage.setItem('dark', 1)
    }else{
        localStorage.removeItem('dark')
    }
    
})

var dark = localStorage.getItem('dark')

if(dark){
    document.body.classList.toggle('dark')
}