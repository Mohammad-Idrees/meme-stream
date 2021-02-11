
function fetchData(){
    fetch('/memes')
    .then(response =>{
        if(!response.ok){
            throw Error("ERROR");
        }
        return response.json();
    }).then(data =>{
        console.log(data)
        const html = data.map(user =>{
            return `
            <article>
                <div class="text">
                    <h6><strong>Created by: </strong>${user.name}</h6>
                    <p>${user.caption}</p>
                </div>
                <div style="text-align: right;">
                    <a href="" class="mb-4 text" data-toggle="modal" data-target="#modalContactForm"><button onClick="reply_click(${user.id})">Edit</button></a>
                </div>
                <img src="${user.url}" onerror="this.src='${'https://memegenerator.net/img/instances/58602367.jpg'}';" />
            </article>
            `;
        }).join('');
        document.querySelector('.grid').insertAdjacentHTML("afterbegin", html);
    }).catch(error =>{
        console.log(error);
    })
}
fetchData();