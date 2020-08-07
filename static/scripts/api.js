document.addEventListener('DOMContentLoaded',()=>{
    input=document.querySelector('input');
    btn=document.querySelector('.exec');
    btn.disabled=true;
    input.oninput=()=> btn.disabled=  input.value.length<1;

    btn.onclick=()=>   request(`${location.protocol}/api/${input.value.toLowerCase()}`,'Country');

    document.querySelectorAll('.exece').forEach(button=>button.onclick=()=>  request(`${location.protocol}/api/${button.dataset.url.substring(4)}`,button.dataset.nm));

});
const request=(url,div)=>{
    const r=new XMLHttpRequest();
    r.open('GET',url);
    r.onerror=()=>{

    }

    r.onload=()=>{
        data=JSON.parse(r.responseText);
        document.querySelector(`#${div}d`).innerHTML=JSON.stringify(data);
    }

    r.onprogress=()=>{

    }
    r.send();
}